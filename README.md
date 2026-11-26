# Sentinel-2 NDVI & Carbon Stock Estimation Pipeline

## 1. Project Overview
This project is a methodological practice for estimating carbon stocks using Sentinel-2 satellite imagery and public carbon density coefficients. 
**Disclaimer:** The estimated results are highly sensitive to the assumptions of the empirical coefficients. This project serves as an engineering workflow demonstration, not a verified carbon credit report.

## 2. Data Source & Methodology
- **Data Source**: Sentinel-2 L2A imagery retrieved via Microsoft Planetary Computer STAC API (Simulating Copernicus Open Access Hub). 
- **NDVI Formula**: `NDVI = (NIR - RED) / (NIR + RED)`, masking out invalid pixels (values <= 0).
- **Carbon Estimation Chain**: 
  1. `Pixel Area` = Calculated from `GeoTransform` (UTM projection).
  2. `Biomass` = Empirical formula `Biomass = a * NDVI + b` (Simulated).
  3. `Carbon Density` = `Biomass * Carbon Fraction (0.5)`.
  4. `Total Carbon` = `Sum(Carbon Density * Pixel Area)`.
- **Coefficient Citation**: 
  * Carbon Fraction: Default value 0.5 (Source: IPCC 2006 Guidelines for National Greenhouse Gas Inventories, Volume 4, Chapter 2).
  * Biomass empirical parameters: Simulated for demonstration (In real projects, parameters must be cited from local forestry standards, e.g., Chinese national standard LY/T 2988-2018).

## 3. Reproducibility
- **Environment**: Python 3.10+, `GDAL>=3.5.0`, `NumPy>=1.21.0`, `Rioxarray>=0.15.0`, `Pystac-client>=0.5.0`. (Run `pip install -r requirements.txt`).
- **Input Sample**: Ensure you have a valid `.tif` file with B04 and B08 bands in the `01_Data` folder.
- **Execution Steps**:
  1. Run `Scenario_1_NDVI.py` to generate the true NDVI image.
  2. Run `day21_carbon_sink.py` to calculate the total carbon stock.
- **Expected Output**: The terminal will print the total carbon stock (in tons), and a GeoTIFF containing the carbon density map will be saved in `03_Outputs`.

## 4. Limitations & Assumptions
- **Coefficient Validation**: The empirical coefficients used are default/simulated values and have NOT been locally validated with field-measured data.
- **Accuracy Assessment**: No accuracy evaluation (e.g., R² or RMSE) was performed due to the lack of ground-truth data.
- **Temporal Scale**: This is a single-temporal and single-region analysis. Time-series analysis and change detection are not included in this version.

## 5. Tech Stack
- Python 3, GDAL/OGR, Rioxarray, Pystac-client, NumPy.
