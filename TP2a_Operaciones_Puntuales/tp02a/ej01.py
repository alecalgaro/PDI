import cv2
import numpy as np
import matplotlib.pyplot as plt
import cvui
import utils as ut


IMAGE_DIR = "../images/"
IMAGE_FILE = "clown.jpg"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)
a, c = 1.5, 100

test_case = np.array([[0, 1, 50, 200, 100], [255, 10, 150, 160, 80]])
#print(test_case)
#print(applyLUT(test_case,[a],[c]))
fig, ((ax11, ax12, ax13),
      (ax21, ax22, ax23)) = plt.subplots(2, 3, layout="constrained")
fig.suptitle("Ej 1: LUT", fontsize=16)
ax11.imshow(imagen, cmap="gray", vmax=255, vmin=0)
ax11.set_title(f"Imagen original")
A1, C1 = [a], [c]
ut.plotLUT(ax12, A1, C1)
ax12.set_title(f"a = {A1[0]:.2f}, c = {C1[0]:.2f}")
ax13.imshow(ut.applyLUT(imagen, A1, C1), cmap="gray", vmax=255, vmin=0)
ax13.set_title(f"S={A1[0]:.2f}*R+({C1[0]})")
ax21.imshow(ut.applyNegative(imagen), cmap="gray", vmax=255, vmin=0)
ax21.set_title(f"Imagen negativa")
A2, C2, Rlims2 = ut.hacerTramos([(150, 100), (200, 250)])
ut.plotLUT(ax22, A2, C2, Rlims2)
ax22.set_title(f"Operacion por tramos")
ax23.imshow(ut.applyLUT(imagen, A2, C2, Rlims2), cmap="gray", vmax=255, vmin=0)
ax23.set_title(f"Resultado de operacion por tramos")
#plt.show()

WINDOW_NAME = "TESTING"
cvui.init(WINDOW_NAME)
fig.canvas.draw()
mplot = np.array(fig.canvas.renderer.buffer_rgba())
while (True):
#    if(cvui.trackbar(img, 10, 10, 200, C_cont, float(0), float(100))):
#        C=C_cont[0]
#        img=computeLog(imagen, C)
#

    # convert canvas to image
    cvui.imshow(WINDOW_NAME, cv2.cvtColor(mplot, cv2.COLOR_RGBA2BGR))
    cvui.update()

    if cv2.waitKey(1) == ord("q"):
        break
