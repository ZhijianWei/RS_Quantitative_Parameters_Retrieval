


# 植被叶片和冠层叶绿素含量高精度反演
## <div align="center"><b><a href="https://github.com/ZhijianWei/RS/blob/main/CCC_Retrieval_WZJ/README.md">English</a> | <a href="https://github.com/ZhijianWei/RS/blob/main/CCC_Retrieval_WZJ/READMEzh.md">简体中文</a></b></div>


#### 作者：魏智健 (南京农业大学) ，如果有任何问题，请随时联系我``18151936092@163.com``📧
**如果这套算法对你有帮助，可以给本项目一个 Star ⭐ ，或者推荐给你的朋友们，谢谢！😊**






##  💻简介
##### 代码库包含不同遥感平台的植被叶绿素含量（LCC或CCC）的定量反演方法，近地面平台主要基于最新的一维辐射传输模型PROSAIL-D，航天平台主要基于CI。近地面平台的代码部分还可用于💥大批量模拟地面高光谱反射率数据的生产及多种叶片和冠层参数的定量反演。💥

* **近地面平台LCC的反演**: 需输入实测冠层光谱反射率文件、叶片及冠层相关参数取值或取值范围
  <br><br>
 * **航空平台CCC的反演**: 需输入哨兵2号多光谱影像文件
<br>

## 🔧依赖库

参考[requirements.txt](requirements.txt)
<br>
<br>
## ⚡使用说明

### * **近地面平台模拟光谱生成和LCC反演功能**：

使用近地面LCC反演功能时，需要安装itertools、prosail等库和相关依赖

    pip install prosail
    pip install more-itertools
    pip install numpy
    pip install numba
    pip install pandas
    pip install scikit-learn


或

    conda install -c conda-forge xxxx
   

pip安装出现问题时推荐使用后者，可以解决很多环境冲突问题。<br><br><br>
其中prosail库包含了叶片辐射传输模型PROSPECT-D和冠层模型4SAIL以及它们的整合版PROSAIL-D，这里我主要重新设计了PROSAIL模型的使用入口:

### `Fieldspec_main.py`

在此脚本中，你可以根据需要反演的植被冠层的实际情况，输入叶片和冠层相关参数，模拟出若干条光谱反射率曲线和待反演参数，再使用RMSEfind函数找出和实测光谱最接近的模拟光谱，附在这条光谱最后的一列参数即为反演出的LCC
<br><br>在此脚本的主代码块中，将三个文件地址替换为模拟光谱存储路径，实测光谱存储路径和最佳检索光谱存储路径，即可实现LCC的高精度反演

    results.to_csv('simulated_spectra.csv', index=False)

    best_LCC_find('simulated_spectra.csv', 'measured_spectrum.csv', 'closest_spectrum.csv')

<br><br><br><br>
**如果想使用基础的模型正演生成光谱和模型反演生成参数功能，可以参考以下代码段进行修改：**
<br><br>
需要反演几个参数就在2101的后面加上几：

    results = np.zeros([self.parameters.shape[0], 2101+2], dtype=float) 

在result的最后附上需要反演的参数索引：（这里以LAI和LCC为例）

    results[i,2101:]=[params[self.LAI_index],params[self.Cab_index]]

最后在主代码块部分放上索引序号：

    model.Cab_index = 6
    model.LAI_index = 1
输出结果即为模拟光谱和预期的反演参数<br><br><br><br>


### 模型参数设置参考



| 参数       | 全称                | 单位      | 最小值 | 最大值 |
|----------|-------------------|---------|-----|-----|
| N        | 氮结构参数             | N/A     | 0.8 | 2.5 |
| cab      | 叶绿素含量（a+b）        | ug/cm2  | 0   | 80  |
| caw      | 叶片等效含水量           | cm      | 0   | 200 |
| car      | 胡萝卜素含量            | ug/cm2  | 0   | 20  |
| cbrown   | 棕色素含量             | NA      | 0   | 1   |
| cm       | 叶片干物质含量           | g/cm2   | 0   | 200 |
| lai      | 叶面积指数             | N/A     | 0   | 10  |
| lidfa    | 叶倾角分布a            | N/A     | -   | -   |
| lidfb    | 叶倾角分布b(椭球体分布时可忽略) | N/A     | -   | -   |
| psoil    | 土壤干湿因子            | N/A     | 0   | 1   |
| rsoil    | 土壤亮度因子            | N/A     | -   | -   |
| hspot    | 热点参数              | N/A     | -   | -   |
| tts      | 太阳天顶角             | deg     | 0   | 90  |
| tto      | 观测天顶角             | deg     | 0   | 90  |
| phi      | 相对天顶角             | deg     | 0   | 360 |
| typelidf | 叶倾角分布类型           | Integer | -   | -   |

#### 说明

由于农作物，灌木的叶角分布类型绝大部分为椭球体分布，故typelidf默认为2，lidfb被忽略，**lidfa即为平均叶倾角MLA**（0度为叶片平行地面，90度为叶片垂直于地面）
<br><br><br>
### * **航天平台CCC反演功能**：

使用航天平台CCC反演功能时，需要安装GDAL库和相关依赖

    pip install GDAL


或

    conda install -c conda-forge xxxx
   

pip安装出现问题时推荐使用后者，可以解决很多环境冲突问题。<br><br><br>

航天平台的CCC反演功能在此脚本中：

    S2_main.py
在此脚本的主代码块中，将输入路径替换为你的哨兵2号影像（tif格式）路径，并设置输出路径：

    image_file = './Sentinel2_image.tif'  # 输入文件路径
    output_file = './ccc_output.tif'  # 输出文件路径

代码会自动计算CCC并生成CCC反演影像产品
<br><br><br>

## 🤗特别感谢：<br>

本套算法的辐射传输模型借鉴了J.Gomez-Dans (NCEO & UCL)的PROSAIL的python重写版本（GitHub链接：https://github.com/jgomezdans/prosail ）
