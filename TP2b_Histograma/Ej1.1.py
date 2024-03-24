import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
cv2.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])

Parámetros:
-images: Es una lista de imágenes de origen, donde cada imagen es de tipo uint8 o float32. 
Debe estar en corchetes, es decir, "[img]".
-channels: Es el índice del canal para el que calculamos el histograma. Si la entrada es una 
imagen en escala de grises, su valor será [0]. Para una imagen en color, puedes pasar [0], [1] o [2] 
para calcular el histograma del canal azul, verde o rojo respectivamente.
-mask: Máscara de imagen. Para encontrar el histograma de la imagen completa se usa "None". 
Pero si se quiere encontrar el histograma de una región particular de la imagen, se puede crear
una máscara binaria de esa región y le pasamos esa máscara.
-histSize: el tamaño del histograma va a ser la cantidad de bins que queremos. Para la escala de 
grises completa, pasamos [256], porque no queremos integrar valores, sino que por cada valor de gris
queremos que haya un bin.
-ranges: el rango de valores que queremos que tome el histograma es de 0 a 256, porque los valores 
de gris van de 0 a 255, entonces usamos [0, 256]. 

El método devuelve un histograma, que es un array multidimensional que contiene la frecuencia de 
ocurrencia de cada valor de intensidad de píxel en la imagen.
"""

"""
Inciso a) 
En la imagen "patron2.tif" que es una imagen con columnas negras y blancas intercaladas, esperamos
que el histograma tenga dos picos, uno en 0 y otro en 255, porque los valores de los píxeles son 0 o 255.

Mientras que en la imagen "patron.tif", que es una imagen en color que va desde rojo hasta azul,
pero que la cargamos en escala de grises, esperamos que el histograma este distribuido en el 
rango, porque los valores de los píxeles son variados.
La intensidad de gris se determina por la luminancia de los colores originales. En general, los 
colores más brillantes se convierten en tonos de gris más claros, mientras que los colores más 
oscuros se convierten en tonos de gris más oscuros.
"""

PATH = '../images/'

# Cargar imagenes
patron = cv2.imread(PATH + 'patron.tif', cv2.IMREAD_GRAYSCALE)
patron2 = cv2.imread(PATH + 'patron2.tif')

# Calcular histogramas
hist_patron = cv2.calcHist([patron], [0], None, [256], [0, 256])
hist_patron2 = cv2.calcHist([patron2], [0], None, [256], [0, 256])

# Graficar histogramas
fig, axs = plt.subplots(1, 2)
axs[0].imshow(patron, cmap='gray')
axs[0].set_title('patron.tif')
axs[1].plot(hist_patron)
axs[1].set_title('Histograma')

fig, axs = plt.subplots(1, 2)
axs[0].imshow(patron2, cmap='gray')
axs[0].set_title('patron2.tif')
axs[1].plot(hist_patron2)
axs[1].set_title('Histograma')

plt.show()
