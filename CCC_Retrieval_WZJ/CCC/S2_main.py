import numpy as np
from osgeo import gdal

def read_image(file_path):
    """读取多波段影像数据"""
    dataset = gdal.Open(file_path)
    bands = [dataset.GetRasterBand(i + 1).ReadAsArray() for i in range(dataset.RasterCount)]
    return np.array(bands), dataset

def calculate_ci(band5, band7):
    """计算CI"""
    return (band7 / (band5 + 1e-5)) - 1

def calculate_ccc(ci):
    """计算CCC"""
    return ci * 47.679 + 0.925

def process_image(image_file, output_file):
    """处理影像并输出结果"""
    # 读取影像（假设波段顺序为 B5, B7）
    bands, dataset = read_image(image_file)

    band5 = bands[4]  # B5波段
    band7 = bands[6]  # B7波段

    # 计算CI
    ci = calculate_ci(band5, band7)

    # 计算CCC
    ccc = calculate_ccc(ci)

    # 去除小于0的值
    ccc_masked = np.where(ccc < 0, 0, ccc)

    # 保存结果
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_file, ccc_masked.shape[1], ccc_masked.shape[0], 1, gdal.GDT_Float32)
    out_dataset.GetRasterBand(1).WriteArray(ccc_masked)
    out_dataset.SetGeoTransform(dataset.GetGeoTransform())  # 复制地理信息
    out_dataset.SetProjection(dataset.GetProjection())  # 复制投影信息
    out_dataset.FlushCache()

    print(f"CCC结果已保存到 {output_file}")

# 示例调用
if __name__ == "__main__":
    image_file = './Sentinel2_image.tif'  # 替换为你的影像文件路径
    output_file = './ccc_output.tif'  # 输出文件路径

    # 处理影像
    process_image(image_file, output_file)
