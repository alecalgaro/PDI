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
D0=np.sqrt((X[0]-fmag.shape[0]//2)**2+(Y[0]-fmag.shape[1]//2)**2)
params = {"W":30, "n":2, "D0":D0}
idealpass=uf.ideal_band_filter(imagen.shape,params,False)
idealreject=uf.ideal_band_filter(imagen.shape,params,True)
butterpass=uf.butterworth_band_filter(imagen.shape,params,False)
butterreject=uf.butterworth_band_filter(imagen.shape,params,True)
params = {"W":0.5, "D0":D0}
gausspass=uf.gaussian_band_filter(imagen.shape,params,False)
gaussreject=uf.gaussian_band_filter(imagen.shape,params,True)

fig, ax = plt.subplots(3, 3, layout="constrained")
ax[0][0].imshow(imagen, cmap="gray", vmax=255, vmin=0)
ax[0][0].set_title("Imagen")
ax[0][1].imshow(fmag, cmap="gray", vmax=255, vmin=0)
ax[0][1].set_title("Espectro magnitud")
ax[0][2].imshow(cfmag)
ax[0][2].set_title("Puntos marcados")
ax[1][0].imshow(idealpass, cmap="gray", vmax=1, vmin=0)
ax[1][0].set_title("Ideal pasa")
ax[1][1].imshow(butterpass, cmap="gray", vmax=1, vmin=0)
ax[1][1].set_title("Butterworth pasa")
ax[1][2].imshow(gausspass, cmap="gray", vmax=1, vmin=0)
ax[1][2].set_title("Gauss pasa")
ax[2][0].imshow(idealreject, cmap="gray", vmax=1, vmin=0)
ax[2][0].set_title("Ideal rechaza")
ax[2][1].imshow(butterreject, cmap="gray", vmax=1, vmin=0)
ax[2][1].set_title("Butterworth rechaza")
ax[2][2].imshow(gaussreject, cmap="gray", vmax=1, vmin=0)
ax[2][2].set_title("Gauss rechaza")

plt.show()
