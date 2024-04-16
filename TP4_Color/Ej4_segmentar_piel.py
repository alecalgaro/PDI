import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import color_slicing as cs
import segment_color_hsv_image as sc_hsv
import segment_color_rgb_sphere as sc_sphere
import hist_channel as hc

"""
Segmentacion de color en los modelos de color RGB y HSV.
Las explicaciones del codigo estan en el archivo Ej4.1.py porque es lo mismo pero con otra imagen.

Usando las imagenes de personas para segmentar la piel:
s01_i08_H_CM.png
s03_i10_H_DM.png
s05_i08_H_LB.png
s06_i13_H_LV.png
s08_i06_H_MA.png
"""

PATH = '../images/'

# Si lo quiero usar desde consola:
# python Ej4_segmentar_piel.py -im nombreImagen.png

DEFAULT_IMAGE = "segmentar_piel.png"    # imagen collage de todas las indicadas en el enunciado

ap = argparse.ArgumentParser() 
ap.add_argument("-im", "--image", required=False, help="path de la imagen a utilizar")
args = vars(ap.parse_args())

image_name = args["image"] if args["image"] else DEFAULT_IMAGE

img = cv2.imread(PATH + image_name)
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

#* Analizar histograma de la imagen original por canales de color
# hist_r, hist_g, hist_b, hist_h, hist_s, hist_v = hc.hist_channel(img)

#* Aplicar el rebanado de color en RGB con el metodo de la esfera
# Definir el color central "a" y el radio R0 de la esfera de color
# a = np.array([99, 122, 165])    # ajutar color de piel
# R0 = 60
# img_sliced_rgb, _ = cs.color_slicing_rgb_sphere(img, a, R0)
img_sliced_rgb, _ = sc_sphere.segment_color_rgb_sphere(img)

#* Aplicar el rebanado de color en HSV
# Se debe encontrar un rango de H y S que contenga los colores de piel, y el V se deja de 0 a 255
# lower = np.array([0, 100, 0])     
# upper = np.array([10, 255, 255])
# img_sliced_hsv, _ = cs.color_slicing_hsv(img, lower, upper)
img_sliced_hsv, _ = sc_hsv.segment_color_hsv_image(img)

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