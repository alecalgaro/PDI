"""
Genere una funcion cuyo resultado sea una imagen donde los pixeles tengan los
colores complementarios a los de la original. Utilice las componentes del modelo
HSV y la imagen "rosas.jpg".

Es analogo a obtener el negativo en imagenes en escala de grises.
En color, el complementario de un color es el opuesto en el circulo de colores.
En la teoria anote que si fuera en HSI, al H tomamos 360° menos el H del px, y para la I 
hacemos 1 menos la I del px, y la saturacion la dejamos igual. 
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import invert_colors as ic
import argparse

PATH = "../images/"

# Si lo quiero usar desde consola:
# python Ej4_segmentar_color.py -im nombreImagen.png

default_img = "rosas.jpg"
# default_img = "pattern.tif"     # patron con colores RGB y CMY para comprobar

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen)

img_inverted = ic.invert_colors(img)

# img = cv2.resize(img, (0,0), fx=2, fy=2)
# img_inverted = cv2.resize(img_inverted, (0,0), fx=2, fy=2)

cv2.imshow("Imagen original", img)
cv2.imshow("Imagen invertida", img_inverted)

cv2.waitKey(0)
cv2.destroyAllWindows()