import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse
import color_slicing as cs
import cvui

"""
Segmentacion de color en una imagen en el modelos de color HSV.

Comentarios:
Para hacer el mismo ejemplo del Ej4 para filtrar la camiseta roja del arbitro, 
utilice los trackbars con los siguientes valores:
H min: 125      H max: 179
S min: 65       S max: 255
V min: 90       V max: 255

Siempre probando ir variando los valores hasta encontrar un resultado aceptable.
En este caso, la segmentacion con RGB obtiene un mejor resultado que con HSV.

Una imagen que sirve para probar que funcione bien es "pattern.tif" que tiene cuadrados con los 
colores RGB y abajo CMY, entonces usando los trackbars se puede probar que se obtengan los 
colores que corresponden. Como son los colores puros, si le bajo el S max o el V max ya se ve 
completo en negro, o detalles asi que se pueden probar. 
"""

# Si lo quiero usar desde consola:
# python Ej5_segmentacion_HSV.py -im nombreImagen.png

PATH = '../images/'

default_img = "futbol.jpg"
# default_img = "pattern.tif"

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen)

WINDOW_NAME = 'Imagen segmentada'
WINDOW_NAME_CONTROLS = 'Controles'
cvui.init(WINDOW_NAME)
cvui.init(WINDOW_NAME_CONTROLS)

UI = np.zeros((580, 350, 3), np.uint8)

# Valores iniciales para los trackbars
h_min = [0]
s_min = [0]
v_min = [0]
h_max = [179]
s_max = [255]
v_max = [255]

while True:
    UI[:] = (49, 52, 49)

    # Crear los trackbars para los valores mínimos y máximos de cada canal de color en HSV
    cvui.text(UI, 10, 30, 'H min')
    cvui.trackbar(UI, 10, 50, 300, h_min, 0, 179)
    cvui.text(UI, 10, 120, 'H max')
    cvui.trackbar(UI, 10, 140, 300, h_max, 0, 179)
    cvui.text(UI, 10, 210, 'S min')
    cvui.trackbar(UI, 10, 230, 300, s_min, 0, 255)
    cvui.text(UI, 10, 300, 'S max')
    cvui.trackbar(UI, 10, 320, 300, s_max, 0, 255)
    cvui.text(UI, 10, 380, 'V min')
    cvui.trackbar(UI, 10, 400, 300, v_min, 0, 255)
    cvui.text(UI, 10, 470, 'V max')
    cvui.trackbar(UI, 10, 490, 300, v_max, 0, 255)

    # Crear los arrays lower y upper
    lower = np.array([h_min[0], s_min[0], v_min[0]])
    upper = np.array([h_max[0], s_max[0], v_max[0]])

    # Aplicar el rebanado de color (la imagen se convierte a HSV en la funcion)
    img_slicing = cs.color_slicing_hsv(img, lower, upper)

    # Mostrar la imagen filtrada y los controles
    cvui.imshow(WINDOW_NAME_CONTROLS, UI)
    cvui.imshow(WINDOW_NAME, img_slicing)

    # Salir del bucle si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()