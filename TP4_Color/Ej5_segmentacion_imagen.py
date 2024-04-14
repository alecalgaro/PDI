import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import argparse
import segment_color_rgb_image as scv_rgb
import segment_color_hsv_image as scv_hsv

PATH = '../images/'

# Si lo quiero usar desde consola:
# python Ej5_segmentacion_imagen.py -im nombreImagen.png -m "modeloDeColor"
# python Ej5_segmentacion_imagen.py -im "futbol.jpg" -m "rgb"

DEFAULT_IMAGE = "futbol.jpg"
# DEFAULT_IMAGE = "pattern.tif"
DEFAULT_MODEL_COLOR = "rgb"

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
ap.add_argument("-m", "--model", required=False, help="modelo de color a utilizar (rgb o hsv)")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else DEFAULT_IMAGE
model_color = args["model"] if args["model"] else DEFAULT_MODEL_COLOR

# Leer la imagen
image = cv2.imread(PATH + nombre_imagen)
img = cv2.imread(PATH + nombre_imagen)

if(model_color == "rgb"):   #* Segmentacion de color en imagen utilizando modelo de color RGB.
    scv_rgb.segment_color_rgb_image(image)
else:   #* Segmentacion de color en imagen utilizando modelo de color HSV.
    scv_hsv.segment_color_hsv_image(image)

"""
Comentarios:

Segmentacion de color en RGB:

    Para hacer el mismo ejemplo del Ej4 para filtrar la camiseta roja del arbitro, 
    utilice los trackbars con los siguientes valores:
    R min: 120      R max: 255
    G min: 0        G max: 70
    B min: 0        B max: 60
    Siempre probando ir variando los valores hasta encontrar un resultado aceptable.

Segmentacion de color en HSV:

    Para hacer el mismo ejemplo del Ej4 para filtrar la camiseta roja del arbitro, 
    utilice los trackbars con los siguientes valores:
    H min: 125      H max: 179
    S min: 65       S max: 255
    V min: 90       V max: 255

    Siempre probando ir variando los valores hasta encontrar un resultado aceptable.
    En este caso, la segmentacion con RGB obtiene un mejor resultado que con HSV.

Una imagen que sirve para probar que funcione bien es "pattern.tif" que tiene cuadrados con los 
colores RGB y abajo CMY, entonces usando los trackbars siempre en 0 o 255 se puede probar que se 
obtengan los colores que corresponden.
"""