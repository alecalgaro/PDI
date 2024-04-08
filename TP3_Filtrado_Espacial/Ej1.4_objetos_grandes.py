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
ksize = 5   # debe ser impar

# Aplicar filtro pasa-bajos con mediana
dst_median = cv2.medianBlur(img, ksize)

# Generar imagen binaria con los objetos de mayor tamaño
# Los px con intensidad mayor a un umbral se ponen en 255 y el resto en 0
_, dst_bin = cv2.threshold(dst_median, 80, 255, cv2.THRESH_BINARY)

# Multiplicar imagen original con imagen binaria
result = img * dst_bin

# Crear un separador como una imagen en blanco, para mostrar las imagenes juntas
separator = np.ones((img.shape[0], 10, 3)) * 255
separator = separator.astype(np.uint8)  # convertir a uint8 para mostrarla con las otras

# Mostrar la imagen original y la filtrada con cv2 en una misma ventana
images_w1 = [img, separator, dst_median]
stacked_image_w1 = np.hstack(images_w1)
cv2.imshow('Original y Filtrada', stacked_image_w1)

# Mostrar la imagen binaria y la imagen resultante en una misma ventana
images_w2 = [dst_bin, separator, result]
stacked_image_w2 = np.hstack(images_w2)
cv2.imshow('Binaria y Resultante', stacked_image_w2)

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

Se podrian agregar trackbars para cambiar el valor de ksize y el umbral de binarización y ver 
como cambia el resultado en tiempo real.
"""