""" Ejercicio 1: Lectura, visualizacion y escritura de imagenes.
1. Realice la carga y visualizacion de diferentes imagenes.
2. Muestre en pantalla informacion sobre las imagenes.
3. Investigue los formatos la imagen y como leer y como escribir un valor puntual
de la imagen.
4. Utilice el pasaje por parametros para especificar la imagen a cargar.
5. Defina y recorte una subimagen de una imagen (vea ROI, Region Of Interest).
6. Investigue y realice una funcion que le permita mostrar varias imagenes en
una sola ventana.
7. Dibuje sobre la imagen lineas, circulos y rectangulos (opcional: defina la posicion 
en base al click del mouse).
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import matplotlib.pyplot as plt
import argparse     # para pasaje de parametros

PATH = "../images/"     # para usar la carpeta images que esta afuera

#? 1. Realice la carga y visualizacion de diferentes imagenes.
#? 2. Muestre en pantalla informacion sobre las imagenes.
image = cv2.imread(PATH + 'cameraman.tif')
image2 = cv2.imread(PATH + 'flores02.jpg')

# Convertimos a RGB para mostrar de forma adecuada con matplotlib (OpenCV usa BGR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

plt.figure()
plt.imshow(image)
plt.title('Cameraman\nDimensions: {}\nType: {}'.format(image.shape, image.dtype))

plt.figure()
plt.imshow(image2)
plt.title('Flores\nDimensions: {}\nType: {}'.format(image2.shape, image2.dtype))

plt.show()

#? 3. Investigue los formatos de la imagen y como leer y escribir un valor puntual de la imagen.

"""
Investigar sobre el formato:
uint8 es un tipo de dato utilizado en programación que representa un entero sin signo (es decir, 
un entero que solo puede ser positivo) de 8 bits.

El rango de valores que puede tomar un uint8 es de 0 a 255. Este tipo de dato es muy común en 
PDI ya que los niveles de intensidad de los píxeles en una imagen suelen representarse en este 
rango. Si tenemos una imagen en escala de grises, cada píxel tendrá un valor de intensidad, y si 
tenemos una imagen en RGB u otro modelo de color de tres canales, cada px tendrá tres valores de
intensidad, uno por canal, donde cada uno es un uint8. Por ejemplo [255, 0, 0]
"""

# Leer y escribir un valor puntual de la imagen.
print('Leer un px de la imagen 1: ', image[0, 0])
# Escribir un px de la imagen.
image[0, 0] = [255, 255, 255]
print('Leer un px de la imagen 1: ', image[0, 0])

#? 4. Utilice el pasaje por parametros para especificar la imagen a cargar.
# (se explica su uso en el ejercicio 8_pasaje_parametros.py de la intro a Python y OpenCV)

# Hecho en un archivo separado para poder ejecutarlo sin el resto del codigo.
# Ver ejercicio1_4.py

#? 5. Defina y recorte una subimagen de una imagen (vea ROI, Region Of Interest).

# ROI o Region of Interest, se refiere a una subsección específica de una imagen que se selecciona 
# para un análisis o procesamiento adicional. En el contexto de PDI, a menudo se recorta una ROI 
# de una imagen más grande para aislar un área específica de interés en la imagen.

subimage = image[100:200, 100:200]
cv2.imshow('Subimagen', subimage)
cv2.waitKey(0)
cv2.destroyAllWindows()

#? 6. Investigue y realice una funcion que le permita mostrar varias imagenes en una sola ventana.

# Hecho en el archivo ejercicio1_6.p.
# Hay una funcion que permite mostrar varias imagenes en distintas ventanas, otra que las 
# muestra en una sola ventana, y otra en una misma ventana pero usando matplotlib.

#? 7. Dibuje sobre la imagen lineas, circulos y rectangulos (opcional: defina la posicion 
#? en base al click del mouse).

# Hecho en el archivo ejercicio1_7.py