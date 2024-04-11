"""
Realce mediante acentuado: utilice la imagen "camino.tif" que se observa desenfocada.
Usted debe mejorar la imagen aplicando un filtro pasa altos de suma 1. 
Compare los resultados de procesar la imagen en los modelos RGB, HSV y HSI.
"""

#* La idea es hacer un realce de la imagen manteniendo el brillo original en cada canal.
#* Eso se mostraba en un ejemplo de pag. 40 del PDF de teoria de color.

#* Deje la explicacion de la funcion cv2.filter2D en el word con anotaciones.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

PATH = "../images/"

img = cv2.imread(PATH + "camino.tif")

cv2.imshow('Camino', img)

#* Kernel o mascara para filtro pasa altos de suma 1 (filtro para realce o acentuado)
mask = np.matrix([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
# mask = np.matrix([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])   # con diagonales
# mask = np.matrix([[-1, -2, -1], [-2, 13, -2], [-1, -2, -1]])

#* --- Realce en el modelo RGB (o BGR) aplicando el filtro a cada canal
# En RGB se aplica el filtro a cada canal por separado
b, g, r = cv2.split(img)
b_f = cv2.filter2D(b, -1, kernel=mask, borderType=cv2.BORDER_REPLICATE)
g_f = cv2.filter2D(g, -1, kernel=mask, borderType=cv2.BORDER_REPLICATE)
r_f = cv2.filter2D(r, -1, kernel=mask, borderType=cv2.BORDER_REPLICATE)

bgr_f = cv2.merge((b_f, g_f, r_f))
cv2.imshow("Realce en RGB", bgr_f)

#* --- Realce en el modelo HSV
# En HSV se aplica el filtro solo al canal V
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
v_f = cv2.filter2D(v, -1, kernel=mask, borderType=cv2.BORDER_REPLICATE)

hsv_f = cv2.merge((h, s, v_f))
bgr_f = cv2.cvtColor(hsv_f, cv2.COLOR_HSV2BGR)

cv2.imshow("Realce en HSV", bgr_f)

#* --- Realce en el modelo HSI
# En HSI se aplica el filtro solo al canal I
hsi = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
h, s, i = cv2.split(hsi)
i_f = cv2.filter2D(i, -1, kernel=mask, borderType=cv2.BORDER_REPLICATE)

hsi_f = cv2.merge((h, s, i_f))
bgr_f = cv2.cvtColor(hsi_f, cv2.COLOR_HLS2BGR)

cv2.imshow("Realce en HSI", bgr_f)

cv2.waitKey(0)
cv2.destroyAllWindows()