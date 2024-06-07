"""
Obtenga el nombre completo, profesion y las siglas de la empresa a la que
pertenece la tarjeta personal de la imagen Tarjeta.jpeg.
"""

import cv2
from reconst_morpho import reconst_morpho
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH = '../images/'
img = cv2.imread(PATH + 'Tarjeta.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Original', img)
# Se usa resize para que funcione mejor la reconstruccion morfologica
img = cv2.resize(img,None,fx=3,fy=3)  

# Binarizar
_,img_bin = cv2.threshold(img, 135, 255, cv2.THRESH_BINARY_INV)

k = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4)) 
img_erode = cv2.morphologyEx(img_bin, cv2.MORPH_ERODE,
                          kernel = k, iterations = 2)

cv2.imshow('Binarizada', img_bin)
cv2.imshow('Paso inicial', img_erode)

# Aplicar reconstruccion morfologica
img_f = reconst_morpho(img_erode, img_bin)

# Invertir
img_f = cv2.bitwise_not(img_f)

# Volver al tamaño original sin resize
# img_f = cv2.resize(img_f,None,fx=1/3,fy=1/3)

cv2.imshow('Resultado final', img_f)

# Redimensionar img_bin al mismo size que img_f
img_bin_resized = cv2.resize(img_bin, (img_f.shape[1], img_f.shape[0]))

# Obtener el resto de datos de la tarjeta
img_rest = cv2.bitwise_and(img_bin_resized, img_f)
img_rest = cv2.bitwise_not(img_rest)

cv2.imshow('Resto', img_rest)

cv2.waitKey(0)
cv2.destroyAllWindows()