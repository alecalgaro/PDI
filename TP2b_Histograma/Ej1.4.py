"""
Ej. opcional: investigar la ecualizacion adaptativa de histogramas CLAHE
(Contrast Limited Adaptive Histogram Equalization).

La ecualización de histograma adaptativa limitada por contraste (CLAHE) es un método de mejora de
contraste que utiliza la ecualización de histograma adaptativa. En contraste con la ecualización de
histograma estándar, en la que cada píxel se trata de la misma manera, independientemente de su
intensidad, la ecualización de histograma adaptativa divide la imagen en regiones o bloques mas 
pequeños llamados "tiles" (tiene un parametro tileGridSize) y aplica la ecualización de histograma 
a cada región. Esto evita el problema de la ampliación excesiva del ruido en áreas de la imagen 
con alto contraste local.

En cada uno de esos bloques mas pequeños (tileSize 8x8 por defecto) CLAHE aplica la ecualizacion 
como siempre, pero se limita a una región pequeña, salvo que haya ruido. Si hay ruido se amplificará.
Para evitar eso, se aplica otro parametro para la limitación del contraste. Si cualquier bin del
histograma está por encima del limite de contraste especificado (por defecto 40), esos px se
recortan y se distribuyen uniformemente a otros bins antes de aplicar la ecualizacion del histograma.
Después de la ecualización, para eliminar los artefactos en los bordes de los bloques generados
se aplica una interpolación bilineal.

Se explica en la documentación oficial de OpenCV:
https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html

Entonces la CLAHE se basa en obtener informacion más local, entonces mejora problemas como vimos
antes donde falla la ecualizacion tradicional (ejercicio 1.3).

Algo que podemos hacer es buscar una imagen donde falla la ecualización tradicional de histograma y 
ver si este metodo adaptativo CLAHE tambien falla o si obtiene mejores resultados.
"""

"""
Con la imagen coins.tif, se puede ver que la ecualización tradicional no es útil, pero con CLAHE
se obtiene un mejor resultado, utilizando los parametros clipLimit=2.0, tileGridSize=(8,8), porque
los valores por defecto no daban un buen resultado.

Abajo dejo una comparacion con el histograma de la imagen original, la imagen ecualizada y el 
histograma de la imagen ecualizada con CLAHE, donde en la de CLAHE se ve que se logra una mejor
distribución de los niveles de grises.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import matplotlib.pyplot as plt

PATH = '../images/'

img = cv2.imread(PATH + "coins.tif", cv2.IMREAD_GRAYSCALE)

img_eq = cv2.equalizeHist(img)  # imagen ecualizada
hist = cv2.calcHist([img],[0],None,[256],[0,256])   # histograma original
hist_eq = cv2.calcHist([img_eq],[0],None,[256],[0,256]) # histograma ecualizado

# Create a CLAHE object (Arguments are optional).
#* Los parametros son opcionales, pero se puede ir probando distintos valores hasta obtener un buen resultado.
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)  # imagen ecualizada con CLAHE
hist_cl1 = cv2.calcHist([cl1],[0],None,[256],[0,256]) # histograma ecualizado con CLAHE

fig, axs = plt.subplots(2, 3)

axs[0,0].imshow(img, cmap='gray')
axs[0,0].set_title('Imagen original')

axs[1,0].plot(hist)
axs[1,0].set_title('Histograma original')

axs[0,1].imshow(img_eq, cmap='gray')
axs[0,1].set_title('Imagen ecualizada')

axs[1,1].plot(hist_eq)
axs[1,1].set_title('Histograma ecualizado')

axs[0,2].imshow(cl1, cmap='gray')
axs[0,2].set_title('Imagen ecualizada con CLAHE')

axs[1,2].plot(hist_cl1)
axs[1,2].set_title('Histograma ecualizado con CLAHE')

plt.show()