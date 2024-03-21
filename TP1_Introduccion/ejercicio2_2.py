"""
    Ejercicio 2: Informacion de intensidad.
    2. Obtenga y grafique los valores de intensidad (perfil de intensidad) sobre una
    determinada fila o columna.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import matplotlib.pyplot as plt

PATH = "../images/"

# Cargar imagen en escala de grises
img = cv2.imread(PATH + "camino.tif", cv2.IMREAD_GRAYSCALE)

plt.figure()
plt.imshow(img, cmap='gray')
plt.title('Imagen en escala de grises')

# Graficar el perfil de intensidad de una fila
fila = img[100, :]  # perfil de intensidad de la fila 100
plt.figure()
plt.plot(fila)
plt.title('Perfil de intensidad de la fila 100')
plt.xlabel('Columna')
plt.ylabel('Intensidad')

# Graficar el perfil de intensidad de una columna
columna = img[:, 100]   # perfil de intensidad de la columna 100
plt.figure()
plt.plot(columna)
plt.title('Perfil de intensidad de la columna 100')
plt.xlabel('Fila')
plt.ylabel('Intensidad')

# Mostrar las graficas
plt.show()