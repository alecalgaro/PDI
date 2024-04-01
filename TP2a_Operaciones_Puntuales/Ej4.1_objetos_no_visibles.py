"""
Utilizando las tecnicas aprendidas, descubra que objetos no estan perceptibles
en la imagen earth.bmp y realce la imagen de forma que los objetos se vuelvan
visibles con buen contraste sin realizar modicaciones sustanciales en el resto
de la imagen.
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

#* Probar otras tecnicas
# Probe usar la imagen en el Ej2 con las transformaciones no lineales (log y potencia) 
# pero se altera demasiado la imagen original.

#* Muestro todas las imagenes obtenidas
cv2.imshow('Imagen original', img)
cv2.imshow('Imagen ecualizada', img_eq)
cv2.imshow('Imagen ecualizada con CLAHE', img_clahe)

cv2.waitKey(0)
cv2.destroyAllWindows()