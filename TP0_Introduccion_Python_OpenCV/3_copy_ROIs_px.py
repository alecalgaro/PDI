import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Copy, extract ROIs and access the value of a pixel

"""
Para copiar imagenes es necesario utilizar la funcion copy(), 
ya que la instruccion "=" asigna la misma direccion de memoria a dos variables,
entonces recordar que en Python al usar "=" no se crea una nueva matriz o imagen
sino que se crea una nueva referencia a la misma matriz o imagen, por lo tanto, si 
se modifica esa "copia" se modifica la original, por eso es importante usar copy() si
no se quiere modificar la imagen original.
"""

import cv2

# Load an image
image = cv2.imread('futbol.jpg')

# Copy the image
image2 = image.copy()

# Extract the region of interest (ROI)
# Si quiero copiar solo una ROI de la imagen, se puede hacer:
# image3 = image[x0:x1, y0:y1].copy()
# donde x0, x1, y0, y1 son las coordenadas de la ROI
image3 = image[100:300, 100:300].copy()

# Access the value of a pixel
# pixel = image[y, x]
value_pixel = image[50, 50]
print(value_pixel)
print(image[0, 0])
# image[y,x] = value_pixel
image[0, 0] = value_pixel
print(image[0, 0])

# Nota: valor_px sera un \uint8" para imagenes de grises mientras que seran 
# 3 valores para imaagenes color (BGR, HSV, etc.)