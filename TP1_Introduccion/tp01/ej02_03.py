import cv2
from matplotlib import pyplot as plt

IMAGE_DIR = "../images/"
IMAGE_FILE = "snowman.png"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)

X0, Y0, X1, Y1 = 10, 120, 550, 300
Y = [int(X*(Y1-Y0)/(X1-X0)+Y0) for X in range(X1-X0)]
X = [i for i in range(X0, X1)]

fig, (ax1, ax2) = plt.subplots(1, 2, layout="constrained")
fig.suptitle("Perfil de intensidad", fontsize=16)
ax2.plot(imagen[Y, X])
ax2.set_title(f"Perfil de intensidad en segmento")
ax1.set_title(f"{IMAGE_DIR}{IMAGE_FILE}")
cv2.line(imagen, (X0, Y0),  (X1, Y1), (255), 5)
ax1.imshow(imagen, cmap="gray")
plt.show()
