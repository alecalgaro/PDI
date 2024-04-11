import cv2
import matplotlib.pyplot as plt

IMAGE_DIR = "../images/"
IMAGE_1_FILE = "futbol.jpg"
IMAGE_2_FILE = "clown.jpg"
imagen1 = cv2.imread(f"{IMAGE_DIR}{IMAGE_1_FILE}")
imagen1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2RGB)
imagen2 = cv2.imread(f"{IMAGE_DIR}{IMAGE_2_FILE}", cv2.IMREAD_GRAYSCALE)

#* Matplotlib
fig, (ax1, ax2) = plt.subplots(1, 2, layout="constrained")
fig.suptitle("Ej 1.2: Informacion en pantalla", fontsize=16)
ax1.imshow(imagen1)
ax1.set_title(f"{IMAGE_1_FILE}: shape={imagen1.shape}, dtype={imagen1.dtype}")
ax2.imshow(imagen2, cmap="gray")
ax2.set_title(f"{IMAGE_2_FILE}: shape={imagen2.shape}, dtype={imagen2.dtype}")
plt.show()
