import cv2
import matplotlib.pyplot as plt

IMAGE_DIR = "../images/"
IMAGE_1_FILE = "futbol.jpg"
ROI_X0, ROI_X1, ROI_Y0, ROI_Y1 = 150, 250, 30, 110
imagen1 = cv2.imread(f"{IMAGE_DIR}{IMAGE_1_FILE}")
imagen1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2RGB)
imagen2 = imagen1[ROI_Y0:ROI_Y1, ROI_X0:ROI_X1]

#* Matplotlib
fig, (ax1, ax2) = plt.subplots(1, 2, layout="constrained")
fig.suptitle("Ej 1.5: Region of Interest", fontsize=16)
ax1.imshow(imagen1)
ax1.set_title(f"{IMAGE_1_FILE}: shape={imagen1.shape}, dtype={imagen1.dtype}")
ax2.imshow(imagen2)
ax2.set_title(f"ROI: shape={imagen2.shape}")
plt.show()
