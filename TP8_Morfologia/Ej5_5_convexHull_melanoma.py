"""
Encuentre y grafique la envoltura convexa del melanoma.
Puede implementar el metodo basado en morfologia matematica, o
utilizar el de OpenCV (algoritmo de Jack Sklansky): cv.convexHull()
"""

import cv2
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import segment_color_hsv_image as s_hsv
import segment_color_rgb_image as s_rgb

PATH = '../images/'
img = cv2.imread(PATH + 'melanoma.jpg')
cv2.imshow('Original Image', img)

# Aplicar umbralizacion para obtener una imagen binaria
# _, img_bin = cv2.threshold(img, img.mean(), 255, cv2.THRESH_BINARY_INV)

# Convertir a escala de grises
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Segmento la imagen por color para mejorar el resultado de la 
# deteccion de bordes (pruebo con trackbars y defino un rango)
# _, _ = s_hsv.segment_color_hsv_image(img)
# img_segm, mask = s_rgb.segment_color_rgb_image(img)

# Defino el rango de color (BGR) para segmentar el melanoma 
# Si cambia la imagen se deberia usar el metodo anterior con los trackbars
lower = np.array([0, 0, 0], dtype=np.uint8)
upper = np.array([255, 255, 181], dtype=np.uint8)
mask = cv2.inRange(img, lower, upper)
cv2.imshow('Mask', mask)

# Aplicar operaciones morfologicas para mejorar la mascara binaria
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=5)
# mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=3)
cv2.imshow('Dilated Mask', mask)

# Detectar bordes
edges = cv2.Canny(mask, 100, 200)

# Aplicar morfologia para engrosar un poquito el borde detectado.
# Se hace porque puede haber pequeñas discontinuidades en el borde
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
edges = cv2.dilate(edges, kernel, iterations=1)

cv2.imshow('Edges', edges)

# Encontrar contornos
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Buscar el contorno mas grande
cnt = max(contours, key=cv2.contourArea)

# Dibujar contorno (en rojo)
cv2.drawContours(img, [cnt], -1, (0, 0, 255), 2)
cv2.imshow('Contour', img)

# Encontrar el envoltorio convexo del contorno
hull = cv2.convexHull(cnt)

# Dibujar el envoltorio convexo (en verde)
cv2.drawContours(img, [hull], -1, (0, 255, 0), 2)

# Mostrar la imagen
cv2.imshow('Convex Hull', img)
cv2.waitKey(0)
cv2.destroyAllWindows()