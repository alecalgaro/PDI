"""
Filtros pasa-altos.

1. Defina mascaras de filtrado pasa-altos cuyos coeficientes sumen 1 y apliquelas
sobre diferentes imagenes. Interprete los resultados.

2. Repita el ejercicio anterior para mascaras cuyos coeficientes sumen 0. Compare
los resultados con los del punto anterior.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse

PATH = "../images/"

# Si lo quiero usar desde consola:
# python Ej2_Filtros_PA.py -im nombreImagen.jpg

default_img = 'cameraman.tif'

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen, cv2.IMREAD_GRAYSCALE)

#* Filtro pasa-altos con coeficientes que suman 1
# Realce de altas frecuencias sin eliminar las bajas frecuencias
mask = np.matrix([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

dst_sum1 = cv2.filter2D(img,-1,mask)

#* Filtro pasa-altos con coeficientes que suman 0
# Realce de altas frecuencias eliminando las bajas frecuencias
mask = np.matrix([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])

dst_sum0 = cv2.filter2D(img,-1,mask)

cv2.imshow('Original', img)
cv2.imshow('Filtro suma 1', dst_sum1)
cv2.imshow('Filtro suma 0', dst_sum0)

cv2.waitKey(0)
cv2.destroyAllWindows()