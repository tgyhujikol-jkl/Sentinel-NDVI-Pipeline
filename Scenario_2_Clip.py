import os
from osgeo import gdal

# 1. 找文件
tif_path = r"C:\Users\王怡婷\Downloads\test\01_Data\Hefei_Real_B04.tif"
shp_path = r"C:\Users\王怡婷\Downloads\test\01_Data\boundary.shp"
out_path = r"C:\Users\王怡婷\Downloads\test\03_Outputs\Clipped_Result.tif"

# 2. 检查文件是否存在（外企防御性编程）
if not os.path.exists(tif_path) or not os.path.exists(shp_path):
    print("❌ 错误：找不到源影像或边界文件，请检查 01_Data！")
else:
    print("开始执行矢量裁剪...")
    # 3. 核心操作：gdal.Warp 按边界裁剪
    try:
        gdal.Warp(
            out_path, 
            tif_path, 
            cutlineDSName=shp_path, 
            cropToCutline=True
        )
        print(f"✅ 裁剪成功！结果已保存至: {out_path}")
    except Exception as e:
        print(f"❌ 裁剪失败: {e}")