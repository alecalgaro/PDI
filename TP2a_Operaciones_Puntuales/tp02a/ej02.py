import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider
import cvui
import utils as ut

IMAGE_DIR = "../images/"
IMAGE_FILE = "rmn.jpg"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)

C, G = 1, 1.00
R = np.arange(0, 256, 1)

fig = plt.figure(tight_layout=True)
fig.suptitle("Ej 2: Transformaciones no lineales", fontsize=16)
gs = gridspec.GridSpec(6, 6)
ax00 = fig.add_subplot(gs[0:4, 0:2])
ax00.imshow(imagen, cmap="gray")
ax00.set_title(f"Imagen original")
ax01 = fig.add_subplot(gs[0:2, 2:4])
log_fn = ax01.plot(R, ut.computeLog(R, C, dtype="uint8"), linewidth=2)
ax01.set(xlim=(0, 256), ylim=(0, 256))
ax01.set_title(f"Funcion logaritmica")
ax02 = fig.add_subplot(gs[0:2, 4:])
log_im = ax02.imshow(ut.computeLog(imagen, C), cmap="gray", vmin=0, vmax=255)
ax02.set_title(f"Transf. Log")
ax11 = fig.add_subplot(gs[2:4, 2:4])
pow_fn = ax11.plot(R, ut.computePow(R, G, C, dtype="uint8"), linewidth=2)
ax11.set_title(f"Funcion potencia")
ax11.set(xlim=(0, 256), ylim=(0, 256))
ax12 = fig.add_subplot(gs[2:4, 4:])
pow_im = ax12.imshow(ut.computePow(imagen, G, C), cmap="gray", vmin=0,
                     vmax=255)
ax12.set_title(f"Transf. Pot")

ax_C = fig.add_subplot(gs[4, :])
ax_G = fig.add_subplot(gs[5, :])
C_sld = Slider(ax=ax_C, label="C", valmin=0.0, valmax=5, valinit=C)
G_sld = Slider(ax=ax_G, label="Gamma", valmin=0.0, valmax=5, valinit=G)

def update(val):
    C = C_sld.val
    G = G_sld.val
    log_fn[0].set_ydata(ut.computeLog(R, C, dtype="uint8"))
    pow_fn[0].set_ydata(ut.computePow(R, G, C, dtype="uint8"))
    log_im.set(data=ut.computeLog(imagen, C), cmap="gray")
    pow_im.set(data=ut.computePow(imagen, G, C), cmap="gray")
    fig.canvas.draw_idle()

C_sld.on_changed(update)
G_sld.on_changed(update)

#WINDOW_NAME = "TESTING"
#cvui.init(WINDOW_NAME)
#C_cont=[C]
#img=computeLog(imagen, C)
#while(True):
#    if(cvui.trackbar(img, 10, 10, 200, C_cont, float(0), float(100))):
#        C=C_cont[0]
#        img=computeLog(imagen, C)
#
#    cvui.imshow(WINDOW_NAME, img)
#    cvui.update()
#
#    if cv2.waitKey(1) == ord("q"):
#        break
plt.show()
