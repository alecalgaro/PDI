import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse
import color_slicing as cs
import cvui

"""
Segmentacion de color en una imagen en el modelos de color RGB.

Comentarios:
Para hacer el mismo ejemplo del Ej4 para filtrar la camiseta roja del arbitro, 
utilice los trackbars con los siguientes valores:
R min: 120      R max: 255
G min: 0        G max: 70
B min: 0        B max: 60
Siempre probando ir variando los valores hasta encontrar un resultado aceptable.

Una imagen que sirve para probar que funcione bien es "pattern.tif" que tiene cuadrados con los 
colores RGB y abajo CMY, entonces usando los trackbars siempre en 0 o 255 se puede probar que se 
obtengan los colores que corresponden.
"""

PATH = '../images/'

# Si lo quiero usar desde consola:
# python Ej5_segmentacion_RGB.py -im nombreImagen.png

default_img = "futbol.jpg"
# default_img = "pattern.tif"

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen)

# Crear una ventana para la imagen y otra para los controles
WINDOW_NAME = 'Imagen segmentada'
WINDOW_NAME_CONTROLS = 'Controles'
cvui.init(WINDOW_NAME)
cvui.init(WINDOW_NAME_CONTROLS)

# Crear una imagen en blanco para los controles
UI = np.zeros((580, 350, 3), np.uint8)

# Valores iniciales para los trackbars
r_min = [0]
g_min = [0]
b_min = [0]
r_max = [255]
g_max = [255]
b_max = [255]

while True:
    UI[:] = (49, 52, 49)

    # Crear los trackbars para los valores minimos y maximos de cada canal de color
    cvui.text(UI, 10, 30, 'R min')
    cvui.trackbar(UI, 10, 50, 300, r_min, 0, 255)
    cvui.text(UI, 10, 120, 'R max')
    cvui.trackbar(UI, 10, 140, 300, r_max, 0, 255)
    cvui.text(UI, 10, 210, 'G min')
    cvui.trackbar(UI, 10, 230, 300, g_min, 0, 255)
    cvui.text(UI, 10, 300, 'G max')
    cvui.trackbar(UI, 10, 320, 300, g_max, 0, 255)
    cvui.text(UI, 10, 380, 'B min')
    cvui.trackbar(UI, 10, 400, 300, b_min, 0, 255)
    cvui.text(UI, 10, 470, 'B max')
    cvui.trackbar(UI, 10, 490, 300, b_max, 0, 255)

    # Crear los arrays lower y upper
    lower = np.array([b_min[0], g_min[0], r_min[0]])
    upper = np.array([b_max[0], g_max[0], r_max[0]])

    # Aplicar el rebanado de color
    img_slicing = cs.color_slicing_rgb_range(img, lower, upper)

    # Mostrar la imagen filtrada y los controles
    cvui.imshow(WINDOW_NAME_CONTROLS, UI)
    cvui.imshow(WINDOW_NAME, img_slicing)

    # Salir del bucle si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()