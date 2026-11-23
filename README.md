# Sentinel-NDVI-Pipeline
# Sentinel-2 NDVI Automated Pipeline (Hefei Region)

## 📌 Overview
This project demonstrates an enterprise-grade automated pipeline for processing real Sentinel-2 satellite imagery. It automatically fetches real satellite data from Microsoft Planetary Computer, masks out invalid pixels (clouds/no-data), calculates the NDVI, and outputs the results along with a professional run log.

## 🛠 Tech Stack
- **Language**: Python 3
- **Geospatial Libraries**: GDAL/OGR, Rioxarray, Pystac-client, NumPy
- **Data Source**: Microsoft Planetary Computer (Sentinel-2 L2A)

## ⚙️ Features
- **Cloud-Native Fetching**: Bypasses traditional data downloading by directly accessing STAC APIs.
- **Robust Error Handling**: Uses `try...except` and the `logging` module to prevent pipeline crashes and record QA/QC status.
- **Data Masking**: Replaces invalid zero-value pixels with `NaN` to ensure statistical accuracy for carbon sink calculations.
- **Dynamic Path Management**: Uses `os.path` for cross-platform compatibility.

## 🚀 How to Run
1. Run `day12_fetch_real_rgb.py` to automatically download real Sentinel-2 bands (B02, B03, B04).
2. Run `day20_final_pipeline.py` to batch process the NDVI calculation.
3. Check the `03_Outputs` folder for resulting GeoTIFFs and `pipeline_run.log` for execution details.
