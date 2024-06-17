import cv2
import numpy as np
import utils.fourier as uf
import matplotlib.pyplot as plt

IMAGE_DIR = "../images/"
IMAGE_FILE = "img_degradada.tif"
#IMAGE_FILE = "HeadCT_degradada.tif"
#IMAGE_FILE = "noisy_moon.jpg"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)

fmag,_,_ = uf.get_dft(imagen)

X, Y = np.where(fmag>215)
cfmag = cv2.cvtColor(fmag, cv2.COLOR_GRAY2RGB)
igns=[]
for i in range(len(X)):
    if ((X[i]-fmag.shape[0]//2)**2+(Y[i]-fmag.shape[1]//2)**2)<100:
        igns.append(i)
X=np.delete(X,igns)
Y=np.delete(Y,igns)
#cfmag[X,Y]=[255,0,0]
for i in range(len(X)):
    cv2.circle(cfmag, (Y[i],X[i]), 5, [255,0,0], 1)

fig, ax = plt.subplots(1, 3, layout="constrained")
ax[0].imshow(imagen, cmap="gray", vmax=255, vmin=0)
ax[0].set_title("Imagen")
ax[1].imshow(fmag, cmap="gray", vmax=255, vmin=0)
ax[1].set_title("Espectro magnitud")
ax[2].imshow(cfmag)
ax[2].set_title("Puntos marcados")

plt.show()
