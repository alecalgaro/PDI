import cv2
import matplotlib.pyplot as plt

IMAGE_DIR = "../images/"
IMAGE_1_FILE = "futbol.jpg"
IMAGE_2_FILE = "clown.jpg"
imagen1 = cv2.imread(f"{IMAGE_DIR}{IMAGE_1_FILE}")
imagen1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2RGB)
imagen2 = cv2.imread(f"{IMAGE_DIR}{IMAGE_2_FILE}", cv2.IMREAD_GRAYSCALE)

"""* El formato uint8 dedica 8 bits a un entero sin signo (0 a 255). Se usa
* para cada valor de intensidad que tenga la imagen.
* En escala de grises, cada pixel adquiere un unico valor.
* En color, cada pixel toma tres valores uint8: uno para rojo, otro para verde
* y otro para azul.
*"""

PX, PY = imagen1.shape[1]//2, imagen1.shape[0]//2
print(f"Lectura del pixel ({PX}, {PY}) de la imagen 1: {imagen1[PY, PX]}")
PX, PY = imagen2.shape[1]//2, imagen2.shape[0]//2
imagen2[PY, PX] = 0

#* Matplotlib
fig, (ax1, ax2) = plt.subplots(1, 2, layout="constrained")
fig.suptitle("Ej 1.3: Valores puntuales", fontsize=16)
ax1.imshow(imagen1)
ax1.set_title(f"{IMAGE_1_FILE}: shape={imagen1.shape}, dtype={imagen1.dtype}")
ax2.imshow(imagen2, cmap="gray")
ax2.set_title(f"{IMAGE_2_FILE}: shape={imagen2.shape}, dtype={imagen2.dtype}")
plt.show()
