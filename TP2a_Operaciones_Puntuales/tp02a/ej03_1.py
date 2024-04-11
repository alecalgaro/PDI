import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider
import utils as ut

IMAGE_DIR = "../images/"
IMAGE_FILE_1 = "clown.jpg"
IMAGE_FILE_2 = "coins.tif"
MASK_FILE = "patron2.tif"

img1 = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE_1}", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE_2}", cv2.IMREAD_GRAYSCALE)
mascara = cv2.imread(f"{IMAGE_DIR}{MASK_FILE}", cv2.IMREAD_GRAYSCALE)
alpha = .25

fig1 = plt.figure(tight_layout=True)
fig1.suptitle("Ej 3: Operaciones aritmeticas", fontsize=16)
gs = gridspec.GridSpec(7, 9)
ax11 = fig1.add_subplot(gs[0:3, 0:3])
ax11.imshow(img1, cmap="gray", vmax=255, vmin=0)
ax11.set_title(f"img1")
ax21 = fig1.add_subplot(gs[3:6, 0:3])
ax21.imshow(img2, cmap="gray", vmax=255, vmin=0)
ax21.set_title(f"img2")
ax_A = fig1.add_subplot(gs[6, :])
A_sld = Slider(ax=ax_A, label="alpha", valmin=0.0, valmax=1.0, valinit=alpha,
               valfmt="%.2f")

ax12 = fig1.add_subplot(gs[0:3, 3:6])
ax12.imshow(ut.suma_promedio([img1,img2]), cmap="gray", vmax=255, vmin=0)
ax12.set_title(f"prom=(img1+img2)/2")

ax13 = fig1.add_subplot(gs[0:3, 6:9])
blend_img = ax13.imshow(ut.blending(img1, img2, alpha), cmap="gray",
                        vmax=255, vmin=0)
ax13.set_title(f"blend=(1-{alpha:.2f})img1+{alpha:.2f}img2")

ax22 = fig1.add_subplot(gs[3:6, 3:6])
ax22.imshow(ut.diferencia(img1, img2, "sum"), cmap="gray", vmax=255, vmin=0)
ax22.set_title(f"dif=(img1-img2+255)/2")

ax23 = fig1.add_subplot(gs[3:6, 6:9])
ax23.imshow(ut.diferencia(img1, img2, "res"), cmap="gray", vmax=255, vmin=0)
ax23.set_title(f"dif=(img1-img2-min)(255/(max-min))")

fig2 = plt.figure(tight_layout=True)
fig2.suptitle("Ej 3: Operaciones aritmeticas - Multiplicacion", fontsize=16)
gs2 = gridspec.GridSpec(1, 3)

ax1 = fig2.add_subplot(gs2[0,0])
ax1.imshow(img1, cmap="gray", vmax=255, vmin=0)
ax1.set_title(f"img1")

ax2 = fig2.add_subplot(gs2[0,1])
ax2.imshow(mascara, cmap="gray", vmax=255, vmin=0)
ax2.set_title(f"mask")

ax3 = fig2.add_subplot(gs2[0,2])
ax3.imshow(ut.multiplicacion(img1, mascara), cmap="gray", vmax=255, vmin=0)
ax3.set_title(f"multiplicacion")

def update(val):
    alpha = A_sld.val
    blend_img.set(data=ut.blending(img1, img2, alpha))
    ax13.set_title(f"blend=(1-{alpha:.2f})img1+{alpha:.2f}img2")
    fig1.canvas.draw_idle()

A_sld.on_changed(update)
plt.show()
