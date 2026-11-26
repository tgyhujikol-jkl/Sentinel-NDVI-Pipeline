

import os
import numpy as np
from osgeo import gdal
from decimal import Decimal, getcontext

# 外企规范 1：设置高精度计算，防止因像素面积过小导致结果被浮点数截断为 0
getcontext().prec = 28

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
ndvi_path = os.path.join(BASE_DIR, "03_Outputs", "Hefei_True_NDVI.tif")
out_path = os.path.join(BASE_DIR, "03_Outputs", "Hefei_Carbon_Stock.tif")

ds = gdal.Open(ndvi_path)
if ds is None:
    raise FileNotFoundError("❌ 致命错误：找不到 NDVI 影像，请先执行情景一计算 NDVI！")

ndvi = ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

# 外企规范 2：经验公式模拟
# 真实项目必须查阅当地树种的林业标准（如：生物量 = a * NDVI + b）
# 这里我们用模拟系数：假设碳密度（吨/公顷）= 500 * NDVI * 0.5
# Carbon Fraction default: 0.5 (Source: IPCC 2006 Guidelines, Vol 4, Ch 2)
# Note: Biomass coefficients here are simulated. Real projects require local standard citations.
carbon_per_ha = (500 * ndvi) * 0.5

# 外企规范 3：业务数据清洗
# 将无植被覆盖区（NDVI <= 0.1，如水体、建筑、裸地）强制设为 NaN
carbon_per_ha[ndvi <= 0.1] = np.nan

# 计算有效植被像素的数量
valid_pixel_count = np.sum(~np.isnan(carbon_per_ha))
print(f"✅ 参与计算的真实植被像素数量: {valid_pixel_count}")

# 外企规范 4：防御性编程（核心拦截）
if valid_pixel_count == 0:
    raise ValueError("❌ 致命错误：未检测到任何有效植被像素，无法核算碳储量！请检查源 NDVI 数据是否真实。")

# 外企规范 5：高精度面积换算（1公顷 = 10000平方米）
geo = ds.GetGeoTransform()
pixel_area_m2 = float(Decimal(str(geo[1])) * Decimal(str(abs(geo[5]))))
pixel_area_ha = pixel_area_m2 / 10000.0

# 计算总碳量（使用 np.nansum 忽略 NaN）
total_carbon_tons = np.nansum(carbon_per_ha * pixel_area_ha)

# 防止浮点误差导致输出 0.00
print(f"🎉 核算完成！该区域总碳储量约为: {total_carbon_tons:.4f} 吨碳")

# 导出碳密度 TIF
driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create(out_path, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)
out_ds.SetGeoTransform(ds.GetGeoTransform())
out_ds.SetProjection(ds.GetProjection())
out_ds.GetRasterBand(1).WriteArray(carbon_per_ha)
out_ds.FlushCache()
out_ds = None