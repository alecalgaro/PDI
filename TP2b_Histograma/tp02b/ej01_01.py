import cv2
import matplotlib.pyplot as plt


IMAGE_DIR = "../images/"
IMAGE_FILE1 = "patron.tif"
IMAGE_FILE2 = "patron2.tif"
imagen1 = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE1}", cv2.IMREAD_GRAYSCALE)
imagen2 = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE2}", cv2.IMREAD_GRAYSCALE)

hist1 = cv2.calcHist([imagen1], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([imagen2], [0], None, [256], [0, 256])

fig1, (ax11, ax12) = plt.subplots(1, 2, layout="constrained")
fig1.suptitle("Imagen 1 e histograma", fontsize=16)
ax11.imshow(imagen1, cmap="gray", vmax=255, vmin=0)
ax12.plot(hist1)

fig2, (ax21, ax22) = plt.subplots(1, 2, layout="constrained")
fig2.suptitle("Imagen 2 e histograma", fontsize=16)
ax21.imshow(imagen2, cmap="gray", vmax=255, vmin=0)
ax22.plot(hist2)
plt.show()
