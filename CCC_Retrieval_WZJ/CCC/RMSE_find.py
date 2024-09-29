import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from scipy import interpolate

def best_LCC_find(simulated_file, measured_file, output_file):
    """
    找到与实测光谱最接近的模拟光谱反射率并保存到Excel文件中。

    :parameters:
    simulated_file (str): 模拟光谱文件路径。
    measured_file (str): 实测光谱文件路径。
    output_file (str): 输出Excel文件路径。
    """
    # 加载模拟和实测光谱数据
    simulated_spectra = pd.read_csv(simulated_file)
    measured_spectrum = pd.read_csv(measured_file)

    # 使用400-800nm范围来找最小RMSE，减少计算量
    wavelengths = np.arange(400, 801)
    simulated_wavelengths = simulated_spectra['Wavelength']#可替换成你自己的列名
    measured_wavelengths = measured_spectrum['Wavelength']
    measured_reflectance = measured_spectrum['Reflectance']

    # 初始化最小RMSE和最接近的光谱索引
    min_rmse = float('inf')
    closest_spectrum_index = -1

    # 遍历所有模拟光谱，计算RMSE
    for index, row in simulated_spectra.iterrows():
        # 只选择400-800nm范围内的数据
        mask = (row['Wavelength'] >= 400) & (row['Wavelength'] <= 800)
        simulated_reflectance = row['Reflectance'][mask]
        simulated_wavelengths_selected = row['Wavelength'][mask]

        # 插值以匹配实测光谱的波长
        interpolated_ref = interpolate.interp1d(simulated_wavelengths_selected, simulated_reflectance, kind='linear')(wavelengths)

        rmse = np.sqrt(mean_squared_error(measured_reflectance[(measured_wavelengths >= 400) & (measured_wavelengths <= 800)], interpolated_ref))
        # 更新最小RMSE和最接近的光谱索引
        if rmse < min_rmse:
            min_rmse = rmse
            closest_spectrum_index = index

    # 获取最接近的光谱数据并将最接近的光谱反射率输出到csv表格
    closest_spectrum = simulated_spectra.iloc[closest_spectrum_index]
    closest_spectrum_df = pd.DataFrame({
        'Wavelength': wavelengths,
        'Reflectance': interpolate.interp1d(closest_spectrum['Wavelength'], closest_spectrum['Reflectance'], kind='linear')(wavelengths)
    })
    closest_spectrum_df.to_csv(output_file, index=False)

    print(r'光谱检索完成')