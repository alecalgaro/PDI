"""
Utilizando las tecnicas aprendidas, descubra que objetos no estan perceptibles
en la imagen earth.bmp y realce la imagen de forma que los objetos se vuelvan
visibles con buen contraste sin realizar modicaciones sustanciales en el resto
de la imagen.
"""

"""
Una opción que se implemento fue la ecualización del histograma, para tener un mejor
contraste en la imagen y poder visualizar los objetos que no se percibian.

Otra opción fue aplicar una transformación lineal con lo que vimos en el ejercicio 1
usando una transformacion lineal cambiando el parámetro "a" para mejorar el contraste, pero
no se logra mejorar mucho la visualización de los objetos.
También se probé usar la imagen en el Ej2 junto con transformaciones no lineales, como la 
logaritmica y la de potencia, con las cuales se observan los objetos no visibles pero se 
altera demasiado la imagen original.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2

PATH = "../images/"

img = cv2.imread(PATH + "earth.bmp", cv2.IMREAD_GRAYSCALE)

#* Version haciendo ecualizacion de histograma
img_eq = cv2.equalizeHist(img)

#* Version con ecualizacion adaptativa (CLAHE)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
img_clahe = clahe.apply(img)

# Se probo con otras opciones usando transformaciones como se menciono en el comentario arriba,
# pero no se obtuvieron mejores resultados. 

#* Muestro todas las imagenes obtenidas
cv2.imshow('Imagen original', img)
cv2.imshow('Imagen ecualizada', img_eq)
cv2.imshow('Imagen ecualizada con CLAHE', img_clahe)

cv2.waitKey(0)
cv2.destroyAllWindows()