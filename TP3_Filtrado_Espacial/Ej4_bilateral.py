"""
Aplique un filtro pasa-bajos de su eleccion y el filtro bilateral a las siguientes imagenes: 
mariposa02.png, flores02.jpg y lapices02.jpg (en escala de grises).

Compare los resultados y explique sus apreciaciones.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import map_coordinates
import argparse

PATH = "../images/"

#* Si lo quiero usar desde consola:
#* python Ej4_bilateral.py -im nombreImagen.jpg

# Imagenes a usar: mariposa02.png, flores02.jpg y lapices02.jpg
# default_img = 'mariposa02.png'
# default_img = 'flores02.jpg'
default_img = 'lapices02.jpg'

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen, cv2.IMREAD_GRAYSCALE)

#* Aplicar el filtro blur (filtro pasa-bajos elegido) con un tamaño de kernel de MxN
M = 3
N = 3
img_blur = cv2.blur(img, (M, N))

#* Aplicar el filtro bilateral con un diametro de 9, sigmaColor de 75 y sigmaSpace de 75
img_bilateral = cv2.bilateralFilter(img, 9, 75, 75)

#* Mostrar la imagen original y las imagenes filtradas
plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original')
# plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_blur, cmap='gray')
plt.title('Blur Filter')
# plt.axis('off')

plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original')
# plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_bilateral, cmap='gray')
plt.title('Bilateral Filter')
# plt.axis('off')

#* Si se quieren mostrar mas grandes con cv2
# cv2.imshow('Original', img)
# cv2.imshow('Blur Filter', img_blur)
# cv2.imshow('Bilateral Filter', img_bilateral)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

"""
Utilice la funcion implementada en la guia anterior para visualizar perfiles de grises, 
eligiendo la misma fila o columna para la imagen original y las que han sido filtradas. 
Compare los resultados visualizandolos simultaneamente.
"""

# Graficar el perfil de intensidad de una fila
id_fila = 200
fila_img = img[id_fila, :]  # perfil de intensidad de la fila indicada
fila_blur = img_blur[id_fila, :]  
fila_bilateral = img_bilateral[id_fila, :]  

plt.figure()
plt.plot(fila_img, 'r', label='Imagen original') 
plt.plot(fila_blur, 'g', label='Blur Filter') 
plt.plot(fila_bilateral, 'b', label='Bilateral Filter') 
plt.title('Perfil de intensidad de la fila ' + str(id_fila))
plt.xlabel('Columna')
plt.ylabel('Intensidad')
plt.legend()  # Agregar leyenda (los label de cada plot)

"""
[Opcional] Implemente una funcion que le permita extraer perfiles de grises de las 3 
imagenes, de cualquier longitud y en cualquier direccion (a partir de clicks del mouse 
o mediante el ingreso de coordenadas) y que realice el ploteo de los perfiles 
superpuestos en diferentes colores.
"""

# Definir dos puntos (y, x)
point1 = (200, 0)
point2 = (200, 600)

# Calcular la cantidad de puntos entre los dos puntos
num_puntos = max(abs(point1[0]-point2[0]), abs(point1[1]-point2[1]))
# Generar los puntos (coordenadas x e y) entre los dos puntos ingresados (linea recta)
x, y = np.linspace(point1[1], point2[1], num_puntos), np.linspace(point1[0], point2[0], num_puntos)

# Extraer el perfil de grises entre los dos puntos de la imagen original y las filtradas 
# -np.vstack((y,x)) crea un array 2D con las coordenadas (y,x) de los puntos interpolados.
# -map_coordinates permite obtener los valores de intensidad (valores de los px) de la imagen en 
# las coordenadas dadas. Devuelve un array 1D con los valores de intensidad de los px.
perfil_img = map_coordinates(img, np.vstack((y,x)))
perfil_blur = map_coordinates(img_blur, np.vstack((y,x)))
perfil_bilateral = map_coordinates(img_bilateral, np.vstack((y,x)))

plt.figure()
plt.plot(perfil_img, 'r', label='Imagen original') 
plt.plot(perfil_blur, 'g', label='Blur Filter') 
plt.plot(perfil_bilateral, 'b', label='Bilateral Filter') 
plt.title('Perfil de intensidad entre ' + str(point1) + " y " + str(point2))
plt.xlabel('Columna')
plt.ylabel('Intensidad')
plt.legend()  # Agregar leyenda (los label de cada plot)

# Mostrar todas las graficas realizadas
plt.show()