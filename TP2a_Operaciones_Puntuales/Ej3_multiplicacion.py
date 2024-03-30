"""
Implemente una funcion que realice las siguientes operaciones aritmeticas
sobre dos imagenes que sean pasadas como parametros:

Multiplicacion. 
En esta operacion la segunda imagen debera ser una mascara binaria (0s y 1s), que se multiplica 
con la primera para muy utilizada como un enmascarado para la extraccion de la region de interes
(ROI) de una imagen. En la imagen de salida solo se veran los px donde la máscara tenía un 1 (blanco)
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

def multiplicacion(img, mask):
    """
    Funcion que realiza la multiplicacion de dos imagenes (una imagen y una mascara binaria).
    """
    result = img * mask
    return result

PATH = "../images/"

# Leer la imagen en escala de grises
img = cv2.imread(PATH + "blister_completo.jpg", cv2.IMREAD_GRAYSCALE)

# Mostrar la imagen original
plt.figure()
plt.imshow(img, cmap='gray')
plt.title('Imagen Original')

# Crear una imagen negra del mismo tamaño que la imagen original
mask = np.zeros(img.shape, dtype=np.uint8)
# Agregar unos (255) la zona de interes para tener una mascara binaria
mask[34:70, 34:70] = 255

plt.figure()
plt.imshow(mask, cmap='gray')
plt.title('Mascara')

# Aplicamos la funcion de multiplicacion
result = multiplicacion(img, mask)

plt.figure()
plt.imshow(result, cmap='gray')
plt.title('Multiplicacion')

plt.show()