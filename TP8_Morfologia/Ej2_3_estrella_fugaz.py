"""
Disene un EE que le permita extraer la estrella fugaz de la imagen
lluviaEstrellas.jpg.
"""

import cv2
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH = '../images/'
img = cv2.imread(PATH + 'lluviaEstrellas.jpg')
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

#* Definir EE
# Como la estrella fugaz es una linea en diagonal de arriba hacia abajo, 
# se puede definir un EE con esa forma.
# Si se aplica un EE de 3x3 funciona pero usando un EE 5x5 se obtiene 
# una imagen mas limpia de la estrella fugaz
ee = np.array([[0, 0, 0, 0, 1],
               [0, 0, 0, 1, 0],
               [0, 0, 1, 0, 0],
               [0, 1, 0, 0, 0],
               [1, 0, 0, 0, 0]], np.uint8)

#* Aplicar erosion con el EE
img_ee = cv2.erode(img, ee)

#* Mostrar imagenes
cv2.imshow('Original', img)
cv2.imshow('Resultado', img_ee)

cv2.waitKey(0)
cv2.destroyAllWindows()