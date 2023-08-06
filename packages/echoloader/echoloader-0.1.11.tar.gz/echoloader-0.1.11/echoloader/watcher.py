import argparse
import base64
import csv
import json
import logging
import math
import os
import re
import socket
import sys
import threading
import time
import traceback
from getpass import getpass
from io import BytesIO
from multiprocessing.dummy import Pool
from pathlib import Path
from time import sleep

import cv2
import numpy as np
import pydicom
import requests
from pycognito import Cognito
from pydicom import uid
from pydicom.encaps import encapsulate
from pydicom.errors import InvalidDicomError
from pydicom.pixel_data_handlers import apply_color_lut
from pynetdicom import AE, evt, ALL_TRANSFER_SYNTAXES
from pynetdicom.sop_class import UltrasoundMultiframeImageStorage, UltrasoundImageStorage
from tqdm import tqdm
from watchdog.events import FileCreatedEvent, FileMovedEvent, FileModifiedEvent
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger('echolog')
OS_VAR_PREFIX = 'US2_'


class AWS:
    def __init__(self, env):
        self.app_url = f'https://{"" if env and env == "production" else env + "-"}app.us2.ai'
        self.service_url = re.sub(r'\bapp\b', 'services', self.app_url)
        self.presign_url = f'{self.service_url}/presign'
        self.app_config = requests.get(f'{self.app_url}/en/assets/config.json').json()
        self.client_id = self.app_config['awsConfig']['aws_user_pools_web_client_id']
        self.user_pool_id = self.app_config['awsConfig']['aws_user_pools_id']


class Us2Cognito(Cognito):
    auth_mutex = threading.Lock()

    def __init__(self, args, username, password):
        super().__init__(args.env.user_pool_id, args.env.client_id, username=username)
        self.authenticate(password=password)
        self.pw = password

    @classmethod
    def get_payload(cls, token):
        payload_text = token.split('.')[1]
        return json.loads(base64.b64decode(payload_text + '===').decode())

    def get_headers(self):
        with self.auth_mutex:
            try:
                self.check_token(renew=True)
            except Exception as exc:
                logger.debug(f"Failed to renew access token due to {exc}, re-authenticating")
                self.authenticate(self.pw)
        return {"Authorization": f"Bearer {self.id_token}"}

    def get_cookies(self):
        return {".idToken": self.id_token}

    def groups(self, prefix="", suffix=""):
        payload = self.get_payload(self.id_token)
        return [s for s in payload.get('cognito:groups', []) if s.startswith(prefix) and s.endswith(suffix)]

    def customer(self):
        groups = self.groups('s3-')
        if groups:
            return groups[0].split('-', 1)[1]
        return self.get_user().sub

    def logout(self):
        return super().logout()

    def join(self):
        pass


def is_video(img=None, shape=None):
    shape = shape or (isinstance(img, np.ndarray) and img.shape)
    return shape and (len(shape) == 4 or (len(shape) == 3 and shape[-1] > 4))


def ybr_to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_YCR_CB2BGR)


def blank_top_bar(media, regions):
    video = is_video(media)
    image = np.mean(media, axis=0) if video else media
    new_image = np.mean(image[..., :3], axis=-1) if 3 <= image.shape[-1] <= 4 else image
    binary_image = (new_image > 2).astype('uint8')
    h = int(binary_image.shape[0] * 0.2)
    sum_pixel = np.sum(binary_image[:h, :], axis=1)
    top_bar = np.where(sum_pixel > (binary_image.shape[0] * 0.88))
    top_bar_bottom = 0
    if len(top_bar[0]) != 0:
        new_image[top_bar, :] = 0
        image[top_bar, :] = 0
        top_bar_bottom = top_bar[0][-1] + 1
    top_bar_bottom = max(top_bar_bottom, 40)
    mask = np.ones_like(media[0] if video else media)
    mask[:top_bar_bottom] = 0
    for region in regions:
        xo, xn = region.RegionLocationMinX0, region.RegionLocationMaxX1
        yo, yn = region.RegionLocationMinY0, region.RegionLocationMaxY1
        mask[yo:yn, xo:xn] = 1
    media *= mask


def parse_dicom_pixel(dicom):
    try:
        px = dicom.pixel_array
    except AttributeError:
        raise InvalidDicomError("No pixel data in dicom")
    pi = dicom.PhotometricInterpretation
    dicom.PhotometricInterpretation = 'RGB'
    if pi in ['YBR_FULL', 'YBR_FULL_422']:
        px = np.asarray([ybr_to_rgb(img) for img in px]) if is_video(px) else ybr_to_rgb(px)
    elif pi in ['PALETTE COLOR']:
        px = (apply_color_lut(px, dicom) // 255).astype('uint8')
    else:
        dicom.PhotometricInterpretation = pi
    blank_top_bar(px, getattr(dicom, "SequenceOfUltrasoundRegions", []))
    return px


def ensure_even(stream):
    # Very important for some viewers
    if len(stream) % 2:
        return stream + b"\x00"
    return stream


def person_data_callback(ds, e):
    if e.VR == "PN" or e.tag == (0x0010, 0x0030):
        del ds[e.tag]


def anonymize_dicom(ds):
    # Populate required values for file meta information
    ds.remove_private_tags()
    ds.walk(person_data_callback)
    media = parse_dicom_pixel(ds)
    video = is_video(media)
    ds.file_meta.TransferSyntaxUID = uid.JPEGBaseline8Bit

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    if len(media.shape) < 3 + video:
        media = np.repeat(np.expand_dims(media, -1), 3, -1)
    ds.Rows, ds.Columns, ds.SamplesPerPixel = media.shape[video:]
    if video:
        ds.StartTrim = 1
        ds.StopTrim = ds.NumberOfFrames = media.shape[0] if video else 1
        ds.CineRate = ds.RecommendedDisplayFrameRate = 63
        ds.FrameTime = 1000 / ds.CineRate
        ds.ActualFrameDuration = math.ceil(1000 / ds.CineRate)
        ds.PreferredPlaybackSequencing = 0
        ds.FrameDelay = 0
    ds.PhotometricInterpretation = "YBR_FULL"
    ds.PixelData = encapsulate([ensure_even(cv2.imencode('.jpg', img)[1].tobytes())
                                for img in (media if video else [media])])
    ds['PixelData'].is_undefined_length = True


def wait_file(path):
    path = Path(path)
    old = None
    cur = os.path.getsize(path)
    while old != cur or not cur:
        sleep(1)
        old, cur = cur, os.path.getsize(path)


class Handler(FileSystemEventHandler):
    def __init__(self, args):
        self.args = args
        self.pool = Pool(args.n)
        self.pbar = tqdm(total=0)
        self.closed = False
        self.write(['customer', 'trial', 'patientID', 'visit', 'filename'])

    def processing(self):
        return self.pbar.n < self.pbar.total

    def write(self, row):
        if self.args.csv_out:
            csv.writer(open(self.args.csv_out, 'a', newline='')).writerow(row)

    def stop(self):
        self.closed = True
        self.pool.terminate()

    def join(self):
        self.pool.join()

    def file_params(self, ds):
        customer = getattr(self.args, 'customer', '')
        return {
            'customer': customer,
            'trial': customer,
            'patient_id': ds.PatientID,
            'visit_id': ds.StudyID or ds.StudyInstanceUID or ds.StudyDate or 'No Study ID',
            'filename': f"{ds.SOPInstanceUID}.dcm",
        }

    def upload(self, ds, params):
        content_type = 'application/dicom'
        params['content_type'] = content_type
        headers = self.args.cognito.get_headers()
        r = requests.post(self.args.env.presign_url, json=params, headers=headers)
        r.raise_for_status()
        url = r.json()
        buf = BytesIO()
        ds.save_as(buf)
        buf.seek(0)
        r = requests.put(url, data=buf.read(), headers={'Content-type': content_type})
        r.raise_for_status()

    def process(self, path=None, ds=None):
        self.pbar.disable = False
        if self.closed:
            return
        path = path and Path(path)
        params = self.file_params(ds or pydicom.dcmread(path, stop_before_pixels=True))
        extracted = self.args.extracted
        k = tuple(params.values())
        if k not in extracted:
            ds = ds or pydicom.dcmread(path)
            if self.args.anonymize:
                anonymize_dicom(ds)
            dst = self.args.dst
            if dst:
                src = self.args.src
                rel = path.relative_to(src)
                out = (dst / rel).with_suffix(".dcm")
                if self.args.overwrite or not out.is_file():
                    out.parent.mkdir(exist_ok=True, parents=True)
                    ds.save_as(out)
            if hasattr(self.args, "cognito"):
                self.upload(ds, params)
            extracted.add(k)
            self.write(k)
        self.pbar.update(1)

    def handle_err(self, err, vargs, kwargs):
        if isinstance(err, InvalidDicomError):
            logger.debug(f'Error during process call: {err}, vargs: {vargs}, kwargs: {kwargs}')
            self.pbar.total -= 1
            self.pbar.update(0)
            return
        logger.error(f'Error during process call: {err}, vargs: {vargs}, kwargs: {kwargs}')
        logger.debug(traceback.format_tb(err.__traceback__))
        self.pbar.update(1)

    def handle(self, *vargs, **kwargs):
        self.pbar.total += 1
        self.pbar.refresh()
        self.pool.apply_async(self.process, vargs, kwargs,
                              error_callback=lambda err: self.handle_err(err, vargs, kwargs))

    def on_any_event(self, event):
        logger.debug(f'got event {event}')
        if isinstance(event, (FileCreatedEvent, FileMovedEvent, FileModifiedEvent)):
            path = event.src_path
            wait_file(path)
            self.handle(path)


def handle_store(event, handler):
    """Handle EVT_C_STORE events."""
    ds = event.dataset
    ds.file_meta = event.file_meta
    handler.handle(ds=ds)
    return 0x0000


def extracted_list(path):
    return {tuple(row) for row in csv.reader(open(path))}


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()


def main():
    parser = argparse.ArgumentParser('EchoLoader')
    parser.add_argument(
        "--src", type=Path,
        help="The folder to anonymize")
    parser.add_argument(
        "--dst",
        help="The output folder for the anonymized DICOM, defaults to src folder suffixed with '_anonymized'")
    parser.add_argument(
        "--watch", action="store_true",
        help="Watch the src folder for changes")
    parser.add_argument(
        "--pacs", action="store_true",
        help="Starts PACS server")
    parser.add_argument(
        "--pacs-ae-title", default="Us2.ai",
        help="PACS AE Title, defaults to Us2.ai")
    parser.add_argument(
        "--pacs-port", default=11112, type=int,
        help="PACS port, defaults to 11112")
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Overwrite files in the output folder")
    parser.add_argument(
        "--n", type=int, default=4,
        help="Number of workers")
    parser.add_argument(
        "--upload", action='store_true',
        help="Will upload all anonymized imaging to Us2.ai cloud")
    parser.add_argument(
        "--env", type=AWS, default=AWS('production'),
        help="The Us2.ai environment to use")
    parser.add_argument(
        "--extracted", type=extracted_list, default=set(),
        help="File of cases to ignore - csv file with customer, trial, patientID, visit, filename")
    parser.add_argument(
        "--csv-out",
        help="Path to csv file of extracted cases")
    parser.add_argument(
        "--verbose", action='store_true',
        help="Path to csv file of extracted cases")
    parser.add_argument(
        '--no-anonymization', action='store_false', dest='anonymize',
        help="No anonymization of data prior to upload"
    )
    args = parser.parse_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
    if args.upload:
        args.cognito = Us2Cognito(
            args,
            os.environ.get(f"{OS_VAR_PREFIX}COGNITO_USERNAME") or input("username: "),
            os.environ.get(f"{OS_VAR_PREFIX}COGNITO_PASSWORD") or getpass("password: "),
        )
        args.customer = args.cognito.groups(prefix='s3-')[0][3:]
    handler = Handler(args)
    try:
        if args.src:
            src = args.src
            paths = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
            args.n = len(paths)
            args.i = 0
            for path in paths:
                handler.handle(path)
            if args.watch:
                logger.warning(f"watching folder {os.path.abspath(src)}")
                src.mkdir(exist_ok=True, parents=True)
                observer = args.observer = Observer()
                observer.schedule(handler, src, recursive=True)
                observer.start()
        if args.pacs:
            logger.warning(
                f"Starting pacs server on {get_ip()}:{args.pacs_port} with AE title {args.pacs_ae_title}")
            handlers = [(evt.EVT_C_STORE, handle_store, [handler])]
            ae = AE()
            ae.add_supported_context(UltrasoundMultiframeImageStorage, ALL_TRANSFER_SYNTAXES)
            ae.add_supported_context(UltrasoundImageStorage, ALL_TRANSFER_SYNTAXES)
            ae.start_server(('0.0.0.0', args.pacs_port), block=True, evt_handlers=handlers, ae_title=args.pacs_ae_title)
        while hasattr(args, 'observer') or handler.processing():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("Interrupted, finishing up jobs")
    finally:
        to_wait = [handler, getattr(args, 'observer', None)]
        to_wait = [e for e in to_wait if e]
        for e in to_wait:
            e.stop()
        for e in to_wait:
            e.join()
