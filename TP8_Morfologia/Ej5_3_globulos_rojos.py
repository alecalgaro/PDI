"""
Se requiere eliminar todos aquellos globulos rojos que esten en contacto, 
directo o indirecto a traves de otro, con el borde.
"""

import cv2
import numpy as np
import reconst_morpho as rec_morpho
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH = '../images/'
img = cv2.imread(PATH + 'globulos_rojos.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Image', img)
cv2.imshow('Image gray', img_gray)

# Threshold the image
# _, img_bin = cv2.threshold(img_gray, img_gray.mean(), 255, cv2.THRESH_BINARY_INV)
print(img_gray.mean())
_, img_bin = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('Thresholded Image', img_bin)

# Crear una mascara de borde
mask = np.zeros_like(img_bin)
mask[0, :] = 255  # Borde superior
mask[-1, :] = 255  # Borde inferior
mask[:, 0] = 255  # Borde izquierdo
mask[:, -1] = 255  # Borde derecho

# Dilatar la mascara de borde
# Mientras mas iteraciones, mas se dilata la mascara del borde, es decir,
# mas se eliminan los globulos rojos que estan cerca del borde
kernel = np.ones((3, 3), np.uint8)
dilated_mask = cv2.dilate(mask, kernel, iterations=1)

# Realizar una reconstruccion morfologica por dilatacion
reconstructed = rec_morpho.reconst_morpho(dilated_mask, img_bin)

# Substraer los globulos rojos conectados al borde
img_final_bin = cv2.subtract(img_bin, reconstructed)

# Dilatacion para agrandar un poquito los lobulos que perdieron un poco 
# de superficie por el thresholding del inicio
# kernel = np.ones((2, 2), np.uint8)
# img_final_bin = cv2.dilate(img_final_bin, kernel, iterations=1)

# Convertir img_final_bin a 3 canales para que la imagen final tenga los lobulos en color
img_final_bin = cv2.cvtColor(img_final_bin, cv2.COLOR_GRAY2BGR)

# Aplicar la mascara a la imagen original para quedarme solo con los lobulos
# que no estan pegados al borde de forma directa o indirecta
img_final = cv2.bitwise_and(img, img_final_bin)

# Mostrar la imagen final
cv2.imshow('Final Image Bin', img_final_bin)
cv2.imshow('Final Image', img_final)
cv2.waitKey(0)
cv2.destroyAllWindows()