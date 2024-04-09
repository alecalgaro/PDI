"""
Filtros de acentuado.
Filtrado por MASCARA DIFUSA.

Obtenga versiones mejoradas de diferentes imagenes mediante el 
filtrado por mascara difusa. Implemente el calculo como:
g(x, y) = f(x, y) - PB(f(x, y))

De la teoria:
Mascara difusa: Es una operación que permite obtener una imagen que 
extrae las altas frecuencias pero con f(x,y) - PB(f(x,y)) que es una 
versión pasa-bajos de la imagen original, osea es una diferencia entre 
una imagen dada f(x, y) y una versión suavizada de la misma imagen 
(una version pasa-bajos), que sería el término PB(f(x,y)). 

Lo que hacemos es eliminar las zonas homogéneas y quedarnos con las 
zonas donde hay más detalles (bordes, altas frecuencias).

En la pág. 20 del PDF de teoria se muestra el ejemplo con la imagen "camaleon.tif".
El resultado que obtuve es el mismo.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse

PATH = "../images/"

# Si lo quiero usar desde consola:
# python Ej3_mascara_difusa.py -im nombreImagen.jpg

default_img = 'camaleon.tif'

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

f = cv2.imread(PATH + nombre_imagen, cv2.IMREAD_GRAYSCALE)

# Filtro pasa-bajos
m_width = 3;
m_height = 3;
kernel = np.ones((m_width,m_height),np.float32)/(m_width*m_height)

PB = cv2.filter2D(f,-1,kernel)

# Aplicar el filtro pasa-altos para filtrado por mascara difusa
g = f - PB

# Ajustar el fondo a gris 127
# En el ejemplo del PDF (pag. 20) se ve que el fondo queda en gris 127, pero aca queda todo negro
# porque el filtro pasa-altos puede producir valores negativos que se truncan a 0 cuando se convierten
# a un formato de imagen de 8 bits, entonces al sumar 127 cambiamos el rango de px de [0, 255] 
# a [127, 382], y cuando se truncan quedan en [127, 255], teniendo un gris 127 de fondo.
g = g + 127

cv2.imshow('Original', f)
cv2.imshow('Pasa bajos', PB)
cv2.imshow('Máscara difusa', g)

cv2.waitKey(0)
cv2.destroyAllWindows()