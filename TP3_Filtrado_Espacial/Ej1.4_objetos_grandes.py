"""
Los filtros pasa-bajos pueden utilizarse para localizar objetos grandes en una
escena. Aplique este concepto a la imagen 'hubble.tif' y obtenga una imagen
de grises cuyos objetos correspondan solamente a los de mayor tamano
de la original.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

PATH = "../images/"

img = cv2.imread(PATH + 'hubble.tif')

# Tamaño del filtro de mediana
ksize = 3   # debe ser impar

# Aplicar filtro pasa-bajos con mediana
dst_median = cv2.medianBlur(img, ksize)

# Mostrar la imagen original y la imagen filtrada
cv2.imshow('Original', img)
cv2.imshow('Median Filter', dst_median)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
Cuanto mas grande es el tamaño del filtro, mas elementos pequeños se eliminan de la imagen, 
pero también se suaviza mas la imagen y se pierden detalles.

Hay otros filtros pasa-bajos que pueden ser utilizados para este propósito, como el filtro
de promediado, filtro gaussiano o filtro bilateral, pero se probó la misma imagen en los incisos
anteriores donde se utilizaron esos otros filtros y el de mediana dio mejor resultado. 

En la pág. 15 del pdf de teoría se ve un ejemplo como este y se dice que luego se puede aplicar
un umbral binario, y que el resultado también sirve para luego aplicar una multiplicación de la
imagen original con la imagen umbralizada para obtener los objetos de mayor tamaño con la calidad
o distribución de grises de la imagen original.
"""

