import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils import fourier as uf

IMAGE_DIR = "../images/"
IMAGE_FILE1 = "cameraman.tif"
imagen1 = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE1}", cv2.IMREAD_GRAYSCALE)
SIGMA = 10
ftype = uf.GAUSSIAN_FILTER

mag_img1, ph_img1, sh_img1 = uf.get_dft(imagen1)
params_id, is_lowpass = {"sigma":SIGMA, "A":2}, False
filt1 = uf.gaussian_filter(imagen1.shape, params_id, is_lowpass)
img_filt1 = uf.apply_filter(imagen1, ftype, params_id, is_lowpass, True)

fig1, ax1 = plt.subplots(1, 3, layout="constrained")
fig1.suptitle("Ej: 3 Filtros", fontsize=16)
ax1[0].imshow(imagen1, cmap="gray", vmax=255, vmin=0)
ax1[0].set_title("Imagen 1")
ax1[1].imshow(filt1, cmap="gray", vmax=1, vmin=0)
ax1[1].set_title("Filtro")
ax1[2].imshow(img_filt1, cmap="gray", vmax=255, vmin=0)
ax1[2].set_title("Imagen filtrada")

plt.show()
