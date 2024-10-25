import requests
import argparse
import logging
from rich.logging import RichHandler
from utils import LogOutputFmt
from pathlib import Path
from bs4 import BeautifulSoup
from rich.progress import track
import exifread
from datetime import datetime
import struct
import time
import hashlib
import requests
import folium

IMAGE_ARCHIVE_A = "https://"
FIRST_IMAGE_A = "001794.jpg"
LAST_IMAGE_A = "003361.jpg"
IMAGE_ARCHIVE_B = "https://"
FIRST_IMAGE_B = "000422.jpg"
LAST_IMAGE_B = "000960.jpg"

TOWER_CACHE = {
    (311, 480, 3, 15770390): False,
    (311, 480, 976, 15770390): False,
    (311, 480, 15620, 15770390): {'lon': -70.823574, 'lat': 43.122402, 'range': 5728},
    (311, 480, 16898, 17003523): {'lon': -72.385569, 'lat': 42.599336, 'range': 1027},
    (311, 480, 15620, 15770391): {'lon': -70.834737, 'lat': 43.129992, 'range': 1956},
    (311, 480, 15620, 15770381): {'lon': -70.893631, 'lat': 43.186111, 'range': 2545},
    (310, 410, 1027, 16656649): {'lon': -72.328613, 'lat': 42.588116, 'range': 1000},
    (310, 410, 1027, 16656649): {'lon': -72.328613, 'lat': 42.588116, 'range': 1000},
    (311, 480, 15620, 15770380): {'lon': -70.887909, 'lat': 43.169403, 'range': 1000},
    (311, 480, 15620, 15770370): {'lon': -70.832839, 'lat': 43.123223, 'range': 2447},
    (310, 410, 1799, 23149064): False,
    (310, 410, 1799, 23149064): False,
    (310, 410, 1027, 16656833): False,
    (310, 410, 1027, 16656813): {'lon': -72.40081, 'lat': 42.604805, 'range': 1000},
    (310, 410, 1027, 16656650): {'lon': -72.328613, 'lat': 42.588116, 'range': 1000},
    (310, 410, 1027, 16656663): False,
}

PRIZE_LOCATIONS = [
    {"lat": 42.59164, "lon": -72.38908, "range":5 },
    {"lat": 43.1443, "lon": -70.8767, "range":5 },
    #{"lat": 43.12708, "lon": -70.87468, "range":5 },
]

class NoWarningsFilter(logging.Filter):
    def filter(self, record):
        return not (record.levelno == logging.WARNING and record.name == 'exifread')

def gen_missing_images(latest: int, first: int) -> list:
    return list(map(img_int_to_name, range(first+1, latest+1)))
    
def img_name_to_int(img_name: str) -> int | None:
    str_name, ext = img_name.split(".", maxsplit=1)
    return int(str_name) if ext == "jpg" else None

def img_int_to_name(num: int) -> str:
    return str(num).zfill(6) + ".jpg"

def latest_image(images: set) -> int:
    return max(images)

def get_latest_images_online(base_url: str) -> list:
    resp = requests.get(f"{base_url}/index.php")
    images = set(map(img_name_to_int, enumerate_images_from_html(resp.text)))
    images.remove(None)
    return images

def enumerate_local_images(dir: Path) -> list:
    images = [x.name for x in dir.glob("*.jpg")]
    images = set(map(img_name_to_int, images))
    return images
    
def enumerate_images_from_html(html_content):
    """
    Enumerate images in HTML content.

    Args:
        html_content (str): The HTML content to parse.

    Yields:
        tuple: Href traget file.
    """

    soup = BeautifulSoup(html_content, 'html.parser')

    for index, img_tag in enumerate(soup.find_all('a'), start=1):
        src = img_tag.get('href')
        if src:
            yield src

def download_image(base_url: str, name: str, out_dir: Path) -> None:
    req = requests.get(f"{base_url}/{name}", allow_redirects=True)
    with open(out_dir / name, mode="wb") as f:
        f.write(req.content)

def config_logging(args:argparse.Namespace) -> None:
    hdlr = RichHandler()
    hdlr.setFormatter(LogOutputFmt())
    logging.basicConfig(level=logging.INFO,format="%(message)s")
    if args.verbose:
        logging.root.setLevel(logging.DEBUG)

    # Get the logger for the module you want to filter
    logger = logging.getLogger('exifread')

    # Add the filter to the logger
    logger.addFilter(NoWarningsFilter())

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
                    prog='Project skydrop script',
                    description='DOwnloads and parses images. Also does some opencv',
                    epilog='Boom goes the dynamite.')
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-ia", "--image_dir_a", type=Path, default=Path("imgs_a"), help="Image directory.")
    parser.add_argument("-ib", "--image_dir_b", type=Path, default=Path("imgs_b"), help="Image directory.")
    parser.add_argument("-o", "--output-map", default="final_map_.html", help="Map filename")
    return parser.parse_args()

def latest_image_local(dir: Path, default: str | None = None) -> int:
    images = enumerate_local_images(dir)
    if not len(images) and default:
        images = set([img_name_to_int(default)-1])
    latest_local = latest_image(images)
    return latest_local
    
def sync_images(args) -> None:
    # What is the most recent image for archive A
    images = get_latest_images_online(IMAGE_ARCHIVE_A)

    latest_online = latest_image(images)
    logging.info(f"[Archive A] Latest image on server: {img_int_to_name(latest_online)}")
    
    # What is the most image we have?
    latest_local = latest_image_local(args.image_dir_a, FIRST_IMAGE_A)
    logging.info(f"Latest image local: {img_int_to_name(latest_local)}")
    
    # Make sure we are up to date locally
    to_download = gen_missing_images(latest_online, latest_local)
    for img in track(to_download, description="Syncing..."):
        download_image(IMAGE_ARCHIVE_A, img, args.image_dir_a)

    # Archive B        
    images = get_latest_images_online(IMAGE_ARCHIVE_B)
    latest_online = latest_image(images)
    logging.info(f"[Archive B] Latest image on server: {img_int_to_name(latest_online)}")
    
    # What is the most image we have?
    latest_local = latest_image_local(args.image_dir_b, FIRST_IMAGE_B)
    logging.info(f"Latest image local: {img_int_to_name(latest_local)}")
    
    # Make sure we are up to date locally
    to_download = gen_missing_images(latest_online, latest_local)
    for img in track(to_download, description="Syncing..."):
        download_image(IMAGE_ARCHIVE_B, img, args.image_dir_b)

    
def generate_md5_hash(data: bytes):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def extract_cell_towers(dir):
    images = enumerate_local_images(dir)
    unq = []
    unq2 = []
    qeng = []
    unq_encs = {}
    # XOR key mask: D2 8B x 512
    flipflip = [ord(x) for x in "\xd2\x8b"*512]
    for img in track(images, description="Extracting cell tower data..."):
        with open(dir / img_int_to_name(img), mode="rb") as f:
            tags = exifread.process_file(f)
            try:
                makernote = bytes(tags["EXIF MakerNote"].values)
                dt = struct.unpack("<HHHHHH", makernote[62:74])
                dt = datetime(dt[5],dt[3],dt[4],dt[2],dt[1],dt[0],)
                # Get logs
                enc = makernote[970:970+1024]
                h = generate_md5_hash(enc)
                if h not in unq:
                    unq.append(h)
                    unq_encs[dt] = enc
                    unq2.append(enc)
                    # decode logs
                    flipflop2 = [x^y for x,y in zip(enc,flipflip)]
                    lines = "".join([chr(x) for x in flipflop2]).split("\n")
                    # save QENG lines
                    for line in lines:
                        if line.startswith("+QENG:"):
                            qeng.append(line)
            except KeyError:
                logging.debug(f"Image {img} does not have proper tags")
                
    logging.info(f"Total images: {len(images)}")
    logging.info(f"Unique data chunnks: {len(unq_encs)}")
    towers = set()
    for line in qeng:
        parts = line.split(",")
        if len(parts) < 13:
            continue
        mcc = int(parts[4])
        mnc = int(parts[5])
        tac = int(parts[12],16)
        cellid = int(parts[6], 16)
        towers.add((mcc, mnc,tac ,cellid))
    return towers

def get_tower_location(mcc: int, mnc: int, lac: int, cell_id: int) -> dict:
    key = (mcc, mnc, lac, cell_id)
    if key in TOWER_CACHE:
        return TOWER_CACHE[key]
    d = {"mcc": mcc, "mnc": mnc, "lac": lac, "cell_id": cell_id}
    url = "https://opencellid.org/ajax/searchCell.php"
    r = requests.get(url, params=d)
    results = r.json()
    logging.info(f"{key}: {results}")
    return results

def map_it(lat: float, long: float, rad: int, m=None, color="blue"):
    loc = [lat, long]
    if m is None:
        m = folium.Map(location=loc, zoom_start=12)
    folium.Circle(location=loc, radius=rad*2, color=color, fill=True, fill_color=color, fill_opacity=0.1).add_to(m)
    return m

def main(args: argparse.Namespace) -> None:
    # Make sure the image image dir exists:
    args.image_dir_a.mkdir(parents=True, exist_ok=True)
    args.image_dir_b.mkdir(parents=True, exist_ok=True)
    sync_images(args)

    map = None
    log_lines = []
    towers = extract_cell_towers(args.image_dir_a)
    for tower in track(towers, description="Geo-locating towers..."):
        log_lines.append(f"MCC: {tower[0]} MNC: {tower[1]} TAC: {tower[2]} CellID: {tower[3]}")
        t_loc = get_tower_location(*tower)
        if t_loc:
            map = map_it(t_loc["lat"], t_loc["lon"], t_loc["range"], map)

    towers = extract_cell_towers(args.image_dir_b)
    for tower in track(towers, description="Geo-locating towers..."):
        log_lines.append(f"MCC: {tower[0]} MNC: {tower[1]} TAC: {tower[2]} CellID: {tower[3]}")
        t_loc = get_tower_location(*tower)
        if t_loc:
            map = map_it(t_loc["lat"], t_loc["lon"], t_loc["range"], map)

    logging.info("Tower Details:")
    for log in log_lines:
        logging.info(log)

    for t_loc in PRIZE_LOCATIONS:
        map = map_it(t_loc["lat"], t_loc["lon"], t_loc["range"], map, "red")
    map.save(args.output_map)
    logging.info(f"Saved map to {args.output_map}")

if __name__ == "__main__":
    args = parse_args()
    config_logging(args)
    main(args)