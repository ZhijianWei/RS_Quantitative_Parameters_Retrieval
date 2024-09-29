import prosail
import numpy as np
import itertools
import pandas as pd
from RMSE_find import best_LCC_find
from scipy.stats import norm


class CartesianProduct:
    def __init__(self, *args):
        self.data = list(args)

    def build(self):
        return list(itertools.product(*self.data))

class ProsailModel:
    def __init__(self, N, Cab, Car, Cb, Cw, Cm, LAI, lidfa, hspot, tts, tto, psi, psoil1):
        """
          :param N :  叶片氮结构参数
          :param Cab:  叶片叶绿素含量
          :param Car:  叶片胡萝卜素含量
          :param Cb:   叶片棕色素含量
          :param Cw:   叶片含水量
          :param Cm:   叶片干物质含量
          :param LAI:  叶面积指数
          :param ldifa:  叶角分布参数,typelidf=2的情况下lidfa便是平均叶倾角
          :param hspot:   热点参数
          :param tts:  太阳天顶角
          :param tto:  太阳方位角
          :param psi:  观测方位角
          :param psoil:  土壤干湿因子，为0完全湿土，为1完全干土

          @ created by Weizhijian, Sunhaoran, 20240522, From NJAU
        """
        self.N = N
        self.Cab = Cab
        self.Car = Car
        self.Cb = Cb
        self.Cw = Cw
        
        self.Cm = Cm
        self.LAI = LAI
        self.lidfa = lidfa
        self.hspot = hspot
        self.tts = tts
        self.tto = tto
        self.psi = psi
        self.psoil1 = psoil1
        self.parameters = self.generate_parameters()

    def generate_parameters(self):
        cartesian_product = CartesianProduct(self.N, self.Cab, self.Car, self.Cb, self.Cw, self.Cm, self.LAI, self.lidfa, self.hspot, self.tts, self.tto, self.psi, self.psoil1)
        return np.array(cartesian_product.build())

    def run_simulations(self):
        results = np.zeros([self.parameters.shape[0], 2101+2], dtype=float) #要展示几个反演参数就加几
        for i, params in enumerate(self.parameters):
            results[i,:2101] = prosail.run_prosail(*params, prospect_version="D", typelidf=2, lidfb=-0.15, rsoil=1,
                                             psoil=params[-1], factor="SDR")
            results[i,2101:]=[params[self.LAI_index],params[self.Cab_index]]
        return results





if __name__ == "__main__":
    #参数取值或取值范围依实际情况而定
    N = np.arange(1, 1.5, 0.1).tolist()
    Cab = [40]
    Car = [10]
    Cb = [0]
    Cw = np.arange(0.003, 0.07, 0.01).tolist()
    Cm = np.arange(0.002, 0.02, 0.001).tolist()
    LAI = np.arange(0, 7.0, 1).tolist()
    lidfa = np.arange(50, 70, 10).tolist()
    hspot = [0.1]
    tts = [60.]
    tto = [0.]
    psi = [0.]
    psoil1 = np.arange(0, 1, 0.1).tolist()

    model = ProsailModel(N, Cab, Car, Cb, Cw, Cm, LAI, lidfa, hspot, tts, tto, psi, psoil1)

    # 以展示叶面积指数LAI和叶片叶绿素含量LCC反演结果为例，反演结果附在模拟光谱文件的最后两列
    model.Cab_index = 6
    model.LAI_index=1
    lengths = [len(param) for param in [N, Cab, Car, Cb, Cw, Cm, LAI, lidfa, [hspot], [tts], [tto], [psi], psoil1]]
    results = model.run_simulations()
    print(results)

    # 计算笛卡尔积的数量，即模拟光谱的数量
    N_simulations = np.prod(lengths)
    print(f"共生成{N_simulations}条模拟光谱")

    #打包功能：将模拟光谱打包成npy文件，可后续深度学习训练使用（耗时较长，仅查看反演结果不需要）
    # np.save('output_file.npy', results)  #替换成你自己的输出路径

    #最佳模拟光谱和叶片/冠层参数检索功能:最佳的反演参数附在最后几列（以本代码的LCC和LAI为例，它们分列最后两列）
    # results.to_csv('simulated_spectra.csv', index=False)
    # best_LCC_find('simulated_spectra.csv', 'measured_spectrum.csv', 'closest_spectrum.csv')#分别替换成模拟光谱存储路径，实测光谱存储路径和反演最佳结果存储路径
