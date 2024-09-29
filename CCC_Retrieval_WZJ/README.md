

# High-Precision Retrieval of Vegetation Leaf and Canopy Chlorophyll Content
## <div align="center"><b><a href="https://github.com/ZhijianWei/RS/blob/main/CCC_Retrieval_WZJ/README.md">English</a> | <a href="https://github.com/ZhijianWei/RS/blob/main/CCC_Retrieval_WZJ/READMEzh.md">Chinese</a></b></div>


#### Author: Zhijian Wei (Nanjing Agricultural University), if you have any questions, please feel free to contact me at ``18151936092@163.com``📧
**If this set of algorithms has helped you, you can give this project a Star ⭐, or recommend it to your friends, thank you!😊**


## 💻Introduction
#### The code library includes quantitative retrieval methods for vegetation chlorophyll content (LCC or CCC) from different remote sensing platforms. Ground-based platforms are mainly based on the latest one-dimensional radiative transfer model PROSAIL-D, while space platforms are primarily based on CI. The code part for ground-based platforms can also be used for 💥large-scale simulation of ground hyperspectral reflectance data production and quantitative retrieval of various leaf and canopy parameters.💥

* **Retrieval of LCC for ground-based platforms**: Requires input of measured canopy spectral reflectance files and leaf and canopy related parameter values or value ranges
  <br><br>
 * **Retrieval of CCC for aviation platforms**: Requires input of Sentinel-2 multispectral image files
<br>
<br>

## 🔧Dependencies

Refer to [requirements.txt](requirements.txt)
<br>
<br>
## ⚡Instructions 

### * **Ground-based platform simulation spectrum generation and LCC retrieval functionality**:

When using the ground-based LCC retrieval function, you need to install libraries such as itertools, prosail, and related dependencies.

    pip install prosail
    pip install more-itertools
    pip install numpy
    pip install numba
    pip install pandas
    pip install scikit-learn

Or

    conda install -c conda-forge xxxx

The latter is recommended when pip installation issues arise, as it can resolve many environment conflict issues.<br><br><br>
The prosail library includes the leaf radiative transfer model PROSPECT-D and the canopy model 4SAIL, as well as their integrated version PROSAIL-D. Here, I have mainly redesigned the entry point for the use of the PROSAIL model:

### `Fieldspec_main.py`

In this script, you can input leaf and canopy related parameters according to the actual situation of the vegetation canopy you need to retrieve, simulate several spectral reflectance curves and parameters to be retrieved, and then use the RMSEfind function to find the simulated spectrum that is closest to the measured spectrum. The parameter in the last column of this spectrum is the retrieved LCC.<br><br>Replace the three file addresses in the main code block of this script with the simulated spectrum storage path, measured spectrum storage path, and the best retrieved spectrum storage path to achieve high-precision retrieval of LCC.

    results.to_csv('simulated_spectra.csv', index=False)

    best_LCC_find('simulated_spectra.csv', 'measured_spectrum.csv', 'closest_spectrum.csv')

<br><br><br><br>
**If you want to use the basic model forward simulation to generate spectra and model inverse retrieval to generate parameters, you can refer to the following code segment for modification:**
<br><br>
Add a few more after 2101 if you need to retrieve several parameters:

    results = np.zeros([self.parameters.shape[0], 2101+2], dtype=float) 

Attach the index of the parameters to be retrieved at the end of the result: (here LAI and LCC are used as examples)

    results[i,2101:]=[params[self.LAI_index],params[self.Cab_index]]

Finally, put the index numbers in the main code block:

    model.Cab_index = 6
    model.LAI_index = 1
The output result will be the simulated spectrum and the expected retrieved parameters<br><br><br><br>


### Model Parameter Settings Reference



| Parameter       | Full Name                | Unit      | Minimum | Maximum |
|----------|-------------------|---------|-----|-----|
| N        | Nitrogen structure parameter             | N/A     | 0.8 | 2.5 |
| cab      | Chlorophyll content (a+b)        | ug/cm2  | 0   | 80  |
| caw      | Leaf equivalent water content           | cm      | 0   | 200 |
| car      | Carotenoid content            | ug/cm2  | 0   | 20  |
| cbrown   | Brown pigment content             | N/A      | 0   | 1   |
| cm       | Leaf dry matter content           | g/cm2   | 0   | 200 |
| lai      | Leaf area index             | N/A     | 0   | 10  |
| lidfa    | Leaf inclination distribution a            | N/A     | -   | -   |
| lidfb    | Leaf inclination distribution b(ignored when elliptical distribution) | N/A     | -   | -   |
| psoil    | Soil moisture factor            | N/A     | 0   | 1   |
| rsoil    | Soil brightness factor            | N/A     | -   | -   |
| hspot    | Hotspot parameter              | N/A     | -   | -   |
| tts      | Sun zenith angle             | deg     | 0   | 90  |
| tto      | Observation zenith angle             | deg     | 0   | 90  |
| phi      | Relative azimuth angle             | deg     | 0   | 360 |
| typelidf | Type of leaf inclination distribution           | Integer | -   | -   |

#### Notes

Since the leaf angle distribution type of most crops and shrubs is ellipsoidal distribution, typelidf defaults to 2, and lidfb is ignored. **lidfa is the mean leaf inclination angle MLA** (0 degrees for leaves parallel to the ground, 90 degrees for leaves perpendicular to the ground)
<br><br><br>
### * **Space-based platform CCC retrieval functionality**:

When using the space-based platform CCC retrieval function, you need to install the GDAL library and related dependencies

    pip install GDAL

Or

    conda install -c conda-forge xxxx

The latter is recommended when pip installation issues arise, as it can resolve many environment conflict issues.<br><br><br>

The CCC retrieval function for the space-based platform is in this script:

    S2_main.py
Replace the input path in the main code block of this script with the path to your Sentinel-2 image (tif format) and set the output path:

    image_file = './Sentinel2_image.tif'  # Input file path
    output_file = './ccc_output.tif'  # Output file path

The code will automatically calculate CCC and generate CCC retrieval image products
<br><br><br>

## 🤗Special Thanks:<br>

The radiative transfer model of this algorithm set refers to J.Gomez-Dans (NCEO & UCL)'s python rewrite version of PROSAIL (GitHub link: [https://github.com/jgomezdans/prosail](https://github.com/jgomezdans/prosail))
