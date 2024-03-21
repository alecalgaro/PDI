"""
    Ejercicio 2: Informacion de intensidad.
    3. Grafique el perfil de intensidad para un segmento de interes cualquiera.
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

# Graficar el perfil de intensidad de un segmento de interes
segmento = img[100:150, 100:150]  # segmento de interes
perfil = segmento.mean(axis=0)  # perfil de intensidad promedio
plt.figure()
plt.plot(perfil)
plt.title('Perfil de intensidad del segmento de interes')
plt.xlabel('Columna')
plt.ylabel('Intensidad')

plt.show()

"""
    Nota: el perfil de intensidad se obtiene promediando los valores de intensidad de cada 
    columna del segmento de interes, por eso usamos mean(axis=0).
"""