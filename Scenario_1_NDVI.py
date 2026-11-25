#                ======情景一：标准NDVI计算完整代码======
#导入必要的库
import os
import glob
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt

#1.找文件
input_dir=r"C:\Users\王怡婷\Downloads\test\01_Data"
#(file_list=glob.glob(r"C:\Users\王怡婷\Downloads\test\01_Data\*.tif"))
file_list=glob.glob(os.path.join(input_dir,"*.tif"))
#2.读取文件
for file in file_list:
    ds=gdal.Open(file)
    if ds is None:
        continue
    #3.读取波段并转浮点型
    red=ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    nir=ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    #4.黑边掩膜
    valid_mask=(red>0)&(nir>0)
    red[~valid_mask]=np.nan
    nir[~valid_mask]=np.nan
    #5.计算NDVI
    ndvi=(nir-red)/(nir+red+1e-10)
    #6.坐标继承
    #out_path=file.replace("01_Data","03_Outputs").replace(".tif","_NDVI.tif")
    filename=os.path.basename(file).replace(".tif","_NDVI.tif")
    out_path=os.path.join(r"C:\Users\王怡婷\Downloads\test\03_Outputs",filename)
    driver=gdal.GetDriverByName('GTiff')
    out_ds=driver.Create(out_path,ds.RasterXSize,ds.RasterYSize,1, gdal.GDT_Float32)
    out_ds.SetProjection(ds.GetProjection())
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    #7.保存
    out_ds.GetRasterBand(1).WriteArray(ndvi)
    out_ds.FlushCache()
    #8.出图
    plt.imshow(ndvi,cmap='RdYlGn')
    plt.colorbar()
    plt.savefig(out_path.replace(".tif",".png"))
    plt.close()
print("NDVI计算完成")


#常规 NDVI 计算与出图（最基础、最常用）

#主管指令：“小王，把这几张影像的 NDVI 算一下，画个图给我看看。”

#· 第 1 步：找文件 -> glob.glob("路径/*.tif")
#· 第 2 步：打开文件 -> gdal.Open(路径)
#· 第 3 步：读波段转浮点 -> ReadAsArray().astype(np.float32)
#· 第 4 步：掩膜去黑边 -> valid_mask = (red > 0) & (nir > 0) 然后赋 np.nan
#· 第 5 步：算公式 -> ndvi = (nir - red) / (nir + red + 1e-10)
#· 第 6 步：坐标继承保存 -> driver.Create + SetGeoTransform + WriteArray
#· 第 7 步：出图 -> plt.imshow + plt.savefig