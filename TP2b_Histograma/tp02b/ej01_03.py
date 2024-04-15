import cv2
import matplotlib.pyplot as plt


IMAGE_DIR = "../images/"
IMAGE_FILE = "earth.bmp"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)

hist = cv2.calcHist([imagen], [0], None, [256], [0, 256])
img_eq = cv2.equalizeHist(imagen)
hist_eq = cv2.calcHist([img_eq], [0], None, [256], [0, 256])

fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2, 2, layout="constrained")
fig.suptitle("Ecualizacion", fontsize=16)
ax11.imshow(imagen, cmap="gray", vmax=255, vmin=0)
ax11.set_title("Imagen original")
ax12.plot(hist)
ax12.set_title("Histograma original")
ax21.imshow(img_eq, cmap="gray", vmax=255, vmin=0)
ax21.set_title("Imagen ecualizada")
ax22.plot(hist_eq)
ax22.set_title("Histograma ecualizado")

plt.show()
