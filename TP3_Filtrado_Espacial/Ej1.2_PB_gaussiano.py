"""
Ejercicio 1: Filtros pasa-bajos.

1.2) 
-Genere mascaras de filtrado gaussianas con diferente sigma (desviacion estandar) y diferente tamaño.
-Visualice y aplique las mascaras sobre una imagen. 
-Compare los resultados con los de un filtro de promediado del mismo tamaño.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse

PATH = "../images/"

# Si lo quiero usar desde consola:
# python Ej1.2_PB_gaussiano.py -im nombreImagen.jpg

default_img = 'placa_ruido_impulsivo.jpg'

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen, cv2.IMREAD_GRAYSCALE)

# Tamano de la mascara 
m_width = 3    # (debe ser impar)
m_height = 3    # (debe ser impar)
sigma = 0

# Aplicar filtro gaussiano
dst = cv2.GaussianBlur(img, (m_width,m_height), sigma)

cv2.imshow('Original', img)
cv2.imshow('Gaussian Blur', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()