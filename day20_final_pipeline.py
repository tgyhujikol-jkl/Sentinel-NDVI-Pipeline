import os
import glob
import logging
import numpy as np
from osgeo import gdal

# 1. 外企核心：配置日志（将运行记录写入文件，并打印到屏幕）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline_run.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 2. 定义核心处理函数（带防御性异常捕获）
def process_image(file_path, out_dir):
    filename = os.path.basename(file_path)
    out_tif = os.path.join(out_dir, f"NDVI_{filename}")
    
    try:
        ds = gdal.Open(file_path)
        if ds is None:
            raise FileNotFoundError(f"打不开影像: {filename}")
            
        red = ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
        nir = ds.GetRasterBand(1).ReadAsArray().astype(np.float32) # 演示用
        
        valid_mask = (red > 0) & (nir > 0)
        red[~valid_mask] = np.nan
        nir[~valid_mask] = np.nan
        
        ndvi = (nir - red) / (nir + red + 1e-10)
        
        driver = gdal.GetDriverByName("GTiff")
        out_ds = driver.Create(out_tif, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)
        out_ds.SetGeoTransform(ds.GetGeoTransform())
        out_ds.SetProjection(ds.GetProjection())
        out_ds.GetRasterBand(1).WriteArray(ndvi)
        out_ds.FlushCache()
        
        logging.info(f"✅ 成功处理: {filename}")
        return True
        
    except Exception as e:
        # 外企核心：捕获异常，程序不闪退，记录错误信息
        logging.error(f"❌ 处理失败 {filename}: {e}")
        return False

# 3. 自动化流水线调度
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "01_Data")
    OUT_DIR = os.path.join(BASE_DIR, "03_Outputs")
    
    logging.info("=== 开始执行自动化流水线 ===")
    file_list = glob.glob(os.path.join(DATA_DIR, "*.tif"))
    
    success_count = 0
    fail_count = 0
    
    for file in file_list:
        if process_image(file, OUT_DIR):
            success_count += 1
        else:
            fail_count += 1
            
    logging.info(f"=== 执行完毕！成功: {success_count}, 失败: {fail_count} ===")
