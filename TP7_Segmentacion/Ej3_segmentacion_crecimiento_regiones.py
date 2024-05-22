"""
Segmentacion mediante crecimiento de regiones.

Implemente el algoritmo siguiendo las indicaciones de la teoria, haciendo
recursiva la funcion de crecimiento.
Como propiedad a cumplir utilice un rango de grises alrededor del valor de
gris de la semilla (cv.inrange()).

Implemente un componente que le permita variar el rango de inclusion y
vicualice el resultado utilizando pseudocolor.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse

PATH = "../images/"

DEFAULT_IMAGE = "rio.jpg"

# Para usar desde consola con parametros
ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

name_image = args["image"] if args["image"] else DEFAULT_IMAGE

img = cv2.imread(PATH + name_image)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def region_growing(img, seed, tol, pseudo=False):
    """
    Algoritmo de crecimiento de regiones.
    
    Parametros:
    - img: imagen a segmentar.
    - seed: coordenadas de la semilla (y, x).
    - tol: tolerancia de gris para la inclusion de pixeles (int).
    - pseudo: si es True retorna imagen con pseudocolor, si es False retorna imagen binaria. 
    
    Retorna:
    - region: imagen con la region segmentada (binaria o con pseudocolor).
    """
    region = np.zeros_like(img)
    region[seed] = 255  # semilla de la region inicial en blanco
    region_size = 1     # tamaño de la region inicial
    mean_region = float(img[seed])  # valor de gris promedio de la region inicial
    
    # Iteramos hasta que no haya pixeles nuevos en la region
    while True:
        # Calculamos los pixeles de borde de la region
        border = cv2.inRange(img, mean_region-tol, mean_region+tol)
        # Excluimos los pixeles que ya estan en la region
        border = cv2.bitwise_and(border, cv2.bitwise_not(region))
        # Si no hay pixeles nuevos en el borde, terminamos
        if cv2.countNonZero(border) == 0:
            break
        region_size += cv2.countNonZero(border)
        mean_region = (mean_region*region_size + np.sum(img[border==255]))/(region_size+cv2.countNonZero(border))
        region[border==255] = 255

    # Aplicamos un mapa de colores a la imagen segmentada si pseudo es True
    if pseudo:
        region = cv2.applyColorMap(region, cv2.COLORMAP_JET)
    return region

#* Variables globales
seed = (0, 0)   # coordenadas de semilla elegida
tol = 10    # tolerancia de gris para la inclusion de pixeles

#* Funcion de callback para elegir una semilla con el clic del mouse
def select_seed(event, x, y, flags, param):
    global seed
    if event == cv2.EVENT_LBUTTONDOWN:
        seed = (y, x)
        # Realizamos la segmentacion de la region cada vez que se hace clic
        region = region_growing(img, seed, tol, pseudo=False)
        cv2.imshow('Segmented', region)

#* Funcion de callback para el trackbar de tolerancia
def update_tol(val):
    global tol
    tol = val

# Registramos la función de callback para el evento de mouse
cv2.namedWindow('Original')
cv2.setMouseCallback('Original', select_seed)

# Creamos un trackbar para ajustar la tolerancia
cv2.createTrackbar('Tolerance', 'Original', tol, 255, update_tol)

# Mostramos la imagen original
cv2.imshow('Original', img)

# Inicializamos la imagen segmentada con una imagen en negro
region = np.zeros_like(img)
cv2.imshow('Segmented', region)

while True:
    # Se ejecuta hasta que se presione la tecla ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()