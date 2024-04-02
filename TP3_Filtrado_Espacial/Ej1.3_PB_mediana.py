"""
Ejercicio 1: Filtros pasa-bajos.

1.3)
-Utilice el filtro de mediana sobre una imagen con diferentes tamaños de ventana.
-Compare los resultados con los filtros anteriores para un mismo tamaño.

El filtro de mediana es un filtro no lineal. Muy utilizado para eliminar ruido impulsivo (sal y 
pimienta), y no genera desenfoque en la imagen como los filtros lineales de suavizado o promediado.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse

PATH = "../images/"

# Si lo quiero usar desde consola:
# python Ej1.3_PB_mediana.py -im nombreImagen.jpg

default_img = "placa_ruido_impulsivo.jpg"
# default_img = "hubble.tif"

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen, cv2.IMREAD_GRAYSCALE)

# Tamano de ventana
ksize = 1   # debe ser impar y mayor a 1

# Aplicar filtro de mediana (filtro no lineal)
dst = cv2.medianBlur(img, ksize)

cv2.imshow('Original', img)
cv2.imshow('Median Blur', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()