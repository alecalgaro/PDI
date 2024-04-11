import cv2
from matplotlib import pyplot as plt

IMAGE_DIR = "../images/"
IMAGE_FILE = "snowman.png"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)
print(imagen.shape)

COL = imagen.shape[1]//2
ROW = imagen.shape[0]//2

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, layout="constrained")
fig.suptitle("Perfiles de intensidad", fontsize=16)

ax2.plot(imagen[:, COL])
ax2.set_title(f"Perfil de intensidad Columna {COL}")
ax3.plot(imagen[ROW, :])
ax3.set_title(f"Perfil de intensidad Fila {ROW}")
ax1.set_title(f"{IMAGE_DIR}{IMAGE_FILE}")
cv2.line(imagen, (COL, 0),  (COL, imagen.shape[0]), (255), 5)
cv2.line(imagen, (0, ROW),  (imagen.shape[1], ROW), (0), 5)
ax1.imshow(imagen, cmap="gray")
plt.show()
