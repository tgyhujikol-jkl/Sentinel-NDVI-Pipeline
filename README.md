# Sentinel-2 NDVI & Carbon Stock Automated Pipeline (Hefei Region)

## 📌 Overview
This project demonstrates an enterprise-grade automated pipeline for processing real Sentinel-2 satellite imagery. It fetches real satellite data from Microsoft Planetary Computer, performs data cleansing (masking out clouds/no-data), calculates the NDVI, and ultimately estimates the regional carbon stock (in tons) based on forestry empirical formulas. 

## 🛠 Tech Stack
- **Language**: Python 3
- **Geospatial Libraries**: GDAL/OGR, Rioxarray, Pystac-client, NumPy
- **Data Source**: Microsoft Planetary Computer (Sentinel-2 L2A)

## ⚙️ Core Features
- **Cloud-Native Fetching**: Bypasses traditional data downloading by directly accessing STAC APIs.
- **Robust Error Handling**: Uses `try...except`, `logging`, and `raise ValueError` assertions to prevent pipeline crashes and ensure data validity (Defensive Programming).
- **Data Masking**: Replaces invalid zero-value pixels with `NaN` to ensure statistical accuracy.
- **High-Precision Calculation**: Utilizes Python's `Decimal` library to prevent float truncation when calculating pixel areas.
- **Carbon Stock Estimation**: Converts NDVI to biomass and carbon stock using empirical formulas, outputting real physical quantities (tons of carbon).

## 📊 Real-World Project Results
- **Max NDVI**: 0.77 (Healthy Vegetation)
- **Min NDVI**: -0.89 (Water Bodies/Clouds)
- **Valid Vegetation Pixels**: 955,205
- **Estimated Total Carbon Stock**: **943,158.94 tons of carbon** 

## 🚀 How to Run
1. Run `day12_fetch_real_rgb.py` to fetch real Sentinel-2 data (B02, B03, B04, B08).
2. Run `Scenario_1_NDVI.py` to calculate the true NDVI using B04 and B08.
3. Run `day21_carbon_sink.py` to estimate the carbon stock.
