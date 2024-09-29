import numpy as np


senile_spectrum = np.load('path_to_senile_spectrum.npy')
green_spectrum = np.load('path_to_green_spectrum.npy')


FS = np.random.random(senile_spectrum.shape)

DHR = senile_spectrum * FS + green_spectrum * (1 - FS)


np.save('path_to_save_DHR.npy', DHR)
print("DHR已保存")