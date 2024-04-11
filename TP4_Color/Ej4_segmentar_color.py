import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import color_slicing as cs
import hist_channel as hc

"""
Segmentacion de color en los modelos de color RGB y HSV.
"""

#! Responder todas las preguntas del enunciado

PATH = '../images/'

# Si lo quiero usar desde consola:
# python Ej4_segmentar_color.py -im nombreImagen.png

default_img = "futbol.jpg"

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

nombre_imagen = args["image"] if args["image"] else default_img

img = cv2.imread(PATH + nombre_imagen)

#* Analizar histograma de la imagen original por canales de color
hist_r, hist_g, hist_b, hist_h, hist_s, hist_v = hc.hist_channel(img)

#* Aplicar el rebanado de color en RGB
# Definir el color central "a" y el radio R0 de la esfera de color
# El color central "a" conviene definirlo tomando un px de la imagen original en la zona donde esta
# el color que nos interesa, porque no siempre sera un color puro.
a = np.array([46, 43, 252])  # rojo de la camiseta del arbitro
R0 = 100
img_sliced_rgb = cs.color_slicing_rgb_sphere(img, a, R0)

#* Aplicar el rebanado de color en HSV
# La funcion recibe una imagen y dos arrays con los valores minimos y maximos de cada canal
# H: 0-179, S: 0-255, V: 0-255
# Como el enunciado pide usar solo los canales H y S, para ignorar el canal V se puede poner
# el rango de 0 a 255 en ese canal.
lower = np.array([0, 100, 0])     
upper = np.array([10, 255, 255])
img_sliced_hsv = cs.color_slicing_hsv(img, lower, upper)

#* Mostrar las imagenes
# Usar matplotlib sirve porque se puede pasar el mouse sobre la imagen y ver los colores [R,G,B]
plt.figure()
plt.subplot(1,3,1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis('off')
plt.subplot(1,3,2)
plt.imshow(cv2.cvtColor(img_sliced_rgb, cv2.COLOR_BGR2RGB))
plt.title('Rebanado de color en RGB')
plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(cv2.cvtColor(img_sliced_hsv, cv2.COLOR_BGR2RGB))
plt.title('Rebanado de color en HSV')
plt.axis('off')
plt.show()