"""
-Repita el proceso (Ej3_1a) para otras imagenes de bajo contraste (por ejemplo
"flowers_oscura.tif") y analice los resultados.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
from eq_hist import eq_hist

PATH = "../images/"

# Cargar las imagenes
img = cv2.imread(PATH + "flowers_oscura.tif")

# Ecualizar la imagen
img_eq = eq_hist(img)

# Mostrar las imagenes
cv2.imshow('Flowers oscura', img)
cv2.imshow('RGB_eq', img_eq[0])
cv2.imshow('HSV_eq', img_eq[1])
cv2.imshow('HSI_eq', img_eq[2])

cv2.waitKey(0)
cv2.destroyAllWindows()

#* Discusion de los resultados:
#* Explicado en el word de anotaciones. 
