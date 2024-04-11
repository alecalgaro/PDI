"""
Habitualmente las imagenes que se relevan en partes no visibles del espectro
(como las de infrarrojos, radar, etc.) se encuentran en escala de grises. Para
resaltar zonas de interes, se pueden asignar colores a rangos especificos de intensidades.
Para este ejercicio debe utilizar la imagen "rio.jpg" y resaltar todas las areas
con acumulaciones grandes de agua (rio central, ramas mayores y pequeños lagos)
en color amarillo.
Se propone una guia metodologica para resolver el ejercicio, con pasos de "a" hasta "d", pero
se puede resolver de otra forma si se prefiere.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import matplotlib.pyplot as plt

PATH = "../images/"

img_rio = cv2.imread(PATH + "rio.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Imagen original", img_rio)

"""
a) Analizar el histograma y estimar el rango de valores en el que se representa el agua.

Analizando el histograma se llega a la conclusión de que el agua se representa con valores de 
intensidad entre 0 y 30 aproximadamente. Por lo tanto, se puede utilizar estos valores para
definir el rango de intensidades que se quiere resaltar en amarillo.
"""

hist_rio = cv2.calcHist([img_rio],[0],None,[256],[0,256])
plt.plot(hist_rio)
plt.show()

"""
b) Generar una imagen color cuyos canales son copia de la imagen de intensidad.
"Imagen de intensidad" es la imagen en escala de grises.
"""

# Crear una nueva imagen en color copiando la imagen de intensidad en cada canal
img_rio_color = cv2.cvtColor(img_rio, cv2.COLOR_GRAY2BGR)
# Otra opcion es con merge colocando la imagen de intensidad en cada canal:
# img_rio_color = cv2.merge([img_rio, img_rio, img_rio])
cv2.imshow("Imagen color", img_rio_color)

"""
c) Recorrer la imagen original y asignar el color amarillo a los pixeles cuyas
intensidades estan dentro del rango definido.

Uso la funcion cv2.inRange() que explique en "0_Intro.py".
Estas lineas las deje comentadas porque en el punto siguiente las implemente con el trackbar.
"""

# Crear una mascara con los pixeles que estan dentro del rango (viendo el histograma)
# mask = cv2.inRange(img_rio, 0, 30)
# cv2.imshow("Mascara", mask)     # blanco en la zona de interes (agua) y el resto negro

# Aplicar la mascara a la imagen color
# img_rio_color[mask == 255] = [0,255,255]    # [0, 255, 255] es amarillo
# cv2.imshow("Imagen con rio amarillo", img_rio_color)

"""
d) Visualizar la imagen resultante y ajustar el rango de grises de ser necesario.
Consejo: esto se hace mas simple utilizando trackbars.

En el inciso "a" se llego a la que el agua se representa con valores de intensidad entre 0 y 30
aproximadamente, entonces en el inciso "c" se asignaron esos valores directamente en la funcion 
inRange para generar la mascara.
Ahora en este ejercicio se ajusta el rango de la mascara usando trackbars para ir probando y ver
como cambia.
"""

min_slider = 0
max_slider = 80
title_window = 'Imagen con rio amarillo'
mask_window = 'Mascara'

def trackbar(val):
    img = img_rio_color.copy()  # crear una copia de la imagen original
    min_val = cv2.getTrackbarPos('Min gris', mask_window)  # obtener el valor del trackbar 'Min gris'
    max_val = cv2.getTrackbarPos('Max gris', mask_window)  # obtener el valor del trackbar 'Max gris'
    mask = cv2.inRange(img_rio, min_val, max_val)     # mascara variable con los trackbars
    img[mask == 255] = [0,255,255]     # aplicar mascara a la imagen color

    cv2.imshow(title_window, img)   # mostrar imagen con mascara aplicada
    cv2.imshow(mask_window, mask)   # mostrar la mascara

cv2.namedWindow(title_window)
cv2.namedWindow(mask_window)
cv2.createTrackbar('Min gris', mask_window, min_slider, max_slider, trackbar)
cv2.createTrackbar('Max gris', mask_window, 30, max_slider, trackbar)

# -----------------------------

cv2.waitKey(0)
cv2.destroyAllWindows()