"""
Manejo de histograma: la imagen "chairs_oscura.jpg" posee poca luminosidad.
Usted debe mejorar la imagen a partir de la ecualizacion de histograma,
comparando los efectos de realizarla en RGB (por planos), en HSV (canal V) y
en HSI (canal I).

-Visualice la imagen original "chairs.jpg", comparela con las imagenes realzadas
y discuta los resultados.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
from eq_hist import eq_hist

PATH = "../images/"

# Cargar las imagenes
img = cv2.imread(PATH + "chairs_oscura.jpg")
img_original = cv2.imread(PATH + "chairs.jpg")
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
img_original = cv2.resize(img_original, (0, 0), fx=0.5, fy=0.5)

# Ecualizar la imagen en los distintos espacios de color
img_eq = eq_hist(img)

# Mostrar las imagenes
cv2.imshow('Chairs oscura', img)
cv2.imshow('Chairs', img_original)

cv2.imshow('RGB_eq', img_eq[0])
cv2.imshow('HSV_eq', img_eq[1])
cv2.imshow('HSI_eq', img_eq[2])

cv2.waitKey(0)
cv2.destroyAllWindows()

#* Discusion de los resultados:
#* Explicado en el word de anotaciones           