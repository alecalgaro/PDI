"""
Filtros de acentuado.
Filtrado por ALTA POTENCIA (high-boost).

Una forma de enfatizar las altas frecuencias (bordes y detalles) sin perder los detalles de bajas
frecuencias (zonas homogéneas) es el filtrado de alta potencia. 
Implemente este procesamiento como la operacion aritmetica:

g(x; y) = Af(x; y) - PB(f(x; y)); con A >= 1:

De la teoria:
La salida "g" es la diferencia entre una version amplificada de la imagen original, usando 
un coeficiente "A", y una version suavizada de la misma imagen (una version pasa-bajos).
La ventaja es que nos da un resultado mas natural que el obtenido utilizando un filtro
pasa-altos de suma 1.

En la pág. 21 y 22 del PDF de teoria se muestran dos ejemplos con la imagen "camaleon.tif".
Usando A=2 y un kernel de 3x3 en el PB da un resultado muy similar al de pag. 21.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse

PATH = "../images/"

# Si lo quiero usar desde consola:
# python Ej3_alta_potencia.py -im nombreImagen.jpg

default_img = 'camaleon.tif'

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

f = cv2.imread(PATH + nombre_imagen, cv2.IMREAD_GRAYSCALE)

# Filtro pasa-bajos
m_width = 3
m_height = 3
kernel = np.ones((m_width,m_height),np.float32)/(m_width*m_height)

PB = cv2.filter2D(f,-1,kernel)

# Aplicar el filtro pasa-altos para filtrado de alta potencia
A = 2
g = A*f - PB

cv2.imshow('Original', f)
cv2.imshow('Pasa bajos', PB)
cv2.imshow('Alta potencia', g)

cv2.waitKey(0)
cv2.destroyAllWindows()
