#                  ===== 情景三：重投影与重采样完整代码 =====
import os
from osgeo import gdal

# 1. 找文件
in_tif = r"C:\Users\王怡婷\Downloads\test\01_Data\Hefei_Real_B04.tif"
out_tif = r"C:\Users\王怡婷\Downloads\test\03_Outputs\WGS84_10m.tif"

# 2. 检查原图
if not os.path.exists(in_tif):
    print("❌ 错误：找不到原图！")
else:
    print("开始执行重投影与重采样...")
    try:
        # 3/4/5/6. 执行转换
        gdal.Warp(
            out_tif, 
            in_tif, 
            dstSRS="EPSG:4326",       # 目标坐标：WGS84经纬度
            xRes=0.0001, yRes=0.0001, # 目标分辨率（度，相当于大概10米）
            resampleAlg="bilinear"    # 插值算法
        )
        print(f"✅ 转换成功！结果已保存至: {out_tif}")
    except Exception as e:
        print(f"❌ 转换失败: {e}")