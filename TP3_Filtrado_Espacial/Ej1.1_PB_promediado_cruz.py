"""
Ejercicio 1: Filtros pasa-bajos.

1.1) Genere diferentes mascaras de promediado, utilizando filtro de promediado o caja 
(box filter) y el formato cruz.
Aplique los filtros sobre una imagen y verifique los efectos de aumentar el tamaño de la 
mascara en la imagen resultante.

Ayuda: mask = np.ones((3,3),np.float32)/9
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse

PATH = "../images/"

#* Si lo quiero usar desde consola:
# python Ej1.1_PB_promediado_cruz.py -im nombreImagen.jpg

#* Si lo quiero ejecutar cambiando la imagen desde el codigo:
# default_img = "placa_ruido_impulsivo.jpg"
default_img = "cameraman.tif"
# default_img = "hubble.tif"    # para probar para el ejercicio 1.4

# Se crea el analizador de parametros y se especican
ap = argparse.ArgumentParser()
# Argumentos que debe esperar el programa 
# (recordar no usar required=True porque sino da error si no se pasa el argumento)   
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
# Se procesan los argumentos de la linea de comandos
args = vars(ap.parse_args())

# Se recuperan en una variable el parametro que queremos o se elige la imagen por defecto si no 
# se paso ninguna por parametros
nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen, cv2.IMREAD_GRAYSCALE)

# Tamano de la mascara
m_width = 3
m_height = 3

#* Crear kernel o mascara de promediado o caja
mask = np.ones((m_width,m_height),np.float32)/(m_width*m_height)

# Aplicar el filtro de promediado con filter2D
dst = cv2.filter2D(img,-1,mask)
# Aplicar el filtro de promediado o caja con boxFilter
dst_box = cv2.boxFilter(img,-1,(m_width,m_height))

#* Crear kernel o mascara de promediado en forma de cruz
# Recordar que los filtros promediadores tienen todos los pesos iguales y suman 1
mask = np.matrix([[0, 1, 0], [1, 1, 1], [0, 1, 0]])*(1/5)
# mask = np.matrix([[0, 0, 1, 0, 0], [1, 1, 1, 1, 1], [0, 0, 1, 0, 0]])*(1/8)

# El otro tipo de filtro de suavizado con pesos distintos era como el de abajo pero no es promediador
# mask = np.matrix([[0, 1/8, 0], [1/8, 1/2, 1/8], [0, 1/8, 0]])

# Aplicar el filtro de promediado en forma de cruz
dst_cross = cv2.filter2D(img,-1,mask)

# Mostrar la imagen original y la imagen obtenida con los filtros de promediado
cv2.imshow('Original', img)
cv2.imshow('Promediado con filter2D', dst)
cv2.imshow('Promediado BoxFilter', dst_box)
cv2.imshow('Promediado Cruz', dst_cross)

cv2.waitKey(0)
cv2.destroyAllWindows()