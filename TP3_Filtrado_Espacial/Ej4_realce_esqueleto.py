"""
Ejercicio de aplicación:

Proponga una combinacion de tecnicas para realzar los detalles de la imagen esqueleto.tif. 
Recuerde que esta tarea es subjetiva y depende de que pretende realzar. 
Justifique cada una de las elecciones en la elaboracion de su propuesta.
"""

"""
Proceso aplicado:
- Se aplica un filtro de mediana (filtro no lineal) para eliminar el ruido impulsivo de la imagen.
- Se aplica una ecualización de histograma adaptativa limitada por contraste (CLAHE) para mejorar 
la visibilidad de los detalles de la imagen, mejorando el contraste local.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import cvui
import numpy as np

PATH = "../images/"

img = cv2.imread(PATH + 'esqueleto.tif', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Original', img)

# Crear una ventana para la imagen y otra para los controles
WINDOW_NAME = 'Imagen final'
WINDOW_NAME_CONTROLS = 'Controles'
cvui.init(WINDOW_NAME)
cvui.init(WINDOW_NAME_CONTROLS)

# Crear una imagen en blanco para los controles
UI = np.zeros((350, 350, 3), np.uint8)

# Inicializar valores
ksize = [1] # Tamaño de ventana para filtro de mediana (debe ser impar)
clipLimit = [2.0]   # Límite de contraste para CLAHE
tileGridSize = [8]  # Tamaño de la cuadrícula para CLAHE

while True:
    UI[:] = (49, 52, 49)

    # Crear trackbars para el tamaño de la ventana, clipLimit y tileGridSize
    cvui.text(UI, 10, 20, 'ksize:')
    cvui.trackbar(UI, 10, 50, 300, ksize, 1, 11, 2)  # El paso es 2
    cvui.text(UI, 10, 120, 'clipLimit:')
    cvui.trackbar(UI, 10, 150, 300, clipLimit, 1, 10)
    cvui.text(UI, 10, 220, 'tileGridSize:')
    cvui.trackbar(UI, 10, 250, 300, tileGridSize, 1, 10)

    # Asegurarse de que ksize sea un número impar
    ksize[0] = int(ksize[0])
    if ksize[0] % 2 == 0:
        ksize[0] += 1

    # Aplicar filtro de mediana
    dst = cv2.medianBlur(img, ksize[0])

    # Crear objeto CLAHE
    clahe = cv2.createCLAHE(clipLimit=clipLimit[0], tileGridSize=(int(tileGridSize[0]), int(tileGridSize[0])))

    # Aplicar ecualización de histograma adaptativa limitada por contraste (CLAHE)
    dst = clahe.apply(dst)

    # Mostrar la imagen filtrada y los controles
    cvui.imshow(WINDOW_NAME, dst)
    cvui.imshow(WINDOW_NAME_CONTROLS, UI)

    # Salir del bucle si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()