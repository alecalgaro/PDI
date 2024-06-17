"""
Utilizando la imagen fosforos.jpg, extraiga en una imagen los fosforos que
estan verticales y en otra los horizontales.
"""

import cv2
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH = '../images/'
img = cv2.imread(PATH + 'fosforos.jpg')
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
cv2.imshow('Original', img)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, img_bin = cv2.threshold(img_gray, img_gray.mean(), 255, cv2.THRESH_BINARY_INV)
cv2.imshow('Binaria', img_bin)

#* EE vertical
EE_v = np.ones((6, 3)).astype('uint8')
EE_v[:,0], EE_v[:,2] = 0,0
print(EE_v)

img_v = cv2.erode(img_bin, EE_v, iterations=3)
img_v = cv2.dilate(img_v, EE_v, iterations=6)

cv2.imshow('Vertical', img_v)

# Aplicar máscara para obtener los fósforos verticales
fosforos_v = cv2.bitwise_and(img, img, mask=img_v) 
cv2.imshow('Fosforos verticales', fosforos_v)

#* EE horizontal
EE_h = np.ones((3, 6)).astype('uint8')
EE_h[0,:], EE_h[2,:] = 0,0
print(EE_h)

img_h = cv2.erode(img_bin, EE_h, iterations=3)
img_h = cv2.dilate(img_h, EE_h, iterations=5)

cv2.imshow('Horizontal', img_h)

# Aplicar máscara para obtener los fósforos horizontales
fosforos_h = cv2.bitwise_and(img, img, mask=img_h)
cv2.imshow('Fosforos horizontales', fosforos_h)

# ---------------------------------------------------------------------

# Invertir las máscaras para cambiar el fondo de negro a blanco
img_v_inv = cv2.bitwise_not(img_v)
img_h_inv = cv2.bitwise_not(img_h)

# Aplicar las máscaras invertidas directamente a la imagen original
fosforos_v_con_fondo_blanco = cv2.bitwise_and(img, img, mask=img_v_inv)
fosforos_h_con_fondo_blanco = cv2.bitwise_and(img, img, mask=img_h_inv)

# Para dejar en blanco las zonas que quedan negras
fosforos_v_con_fondo_blanco[img_v_inv == 0] = 255
fosforos_h_con_fondo_blanco[img_h_inv == 0] = 255

cv2.imshow('Fosforos verticales con fondo blanco', fosforos_v_con_fondo_blanco)
cv2.imshow('Fosforos horizontales con fondo blanco', fosforos_h_con_fondo_blanco)

cv2.waitKey(0)
cv2.destroyAllWindows()