import os
import logging
import planetary_computer as pc
from pystac_client import Client
import rioxarray

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(BASE_DIR, "01_Data")

def fetch_rgb_bands():
    logging.info("正在连接微软 Planetary Computer...")
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        intersects={"type": "Point", "coordinates": [117.2, 31.8]},
        datetime="2023-06-01/2023-08-31",
        query={"eo:cloud_cover": {"lt": 10}}
    )
    items = list(search.items())
    item = items[0]
    signed_item = pc.sign(item)

    for band_name in ["B04", "B03", "B02"]:
        logging.info(f"正在下载 {band_name} 波段...")
        url = signed_item.assets[band_name].href
        data = rioxarray.open_rasterio(url)
        cy, cx = data.rio.height // 2, data.rio.width // 2
        sliced = data.isel(y=slice(cy-512, cy+512), x=slice(cx-512, cx+512))
        out_path = os.path.join(DATA_DIR, f"Hefei_Real_{band_name}.tif")
        sliced.rio.to_raster(out_path)
        logging.info(f"✅ {band_name} 已保存至 {out_path}")

if __name__ == "__main__":
    fetch_rgb_bands()
