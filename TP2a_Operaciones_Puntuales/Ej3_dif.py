"""
Implemente una funcion que realice las siguientes operaciones aritmeticas
sobre dos imagenes que sean pasadas como parametros:

-Diferencia. 
Aplique las dos funciones de reescalado usadas tipicamente para evitar el desborde 
de rango (sumar 255 y dividir por 2, o restar el minimo y escalar a 255).

En el archivo Ej3_dif_v2 deje otra version usando la funcion cv2.subtract (explique la diferencia),
y en el cual se usa un listado de imagenes o frames de un video.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

def difference(img1, img2, rescale_method='add'):
    # Asegurarse de que las imágenes tienen el mismo tamaño
    assert img1.shape == img2.shape, "Las imágenes deben tener el mismo tamaño"

    # Convertir las imagenes a int16 para evitar desbordamiento, ya que la resta puede dar valores 
    # negativos y se vuelven positivos. Con int16 se permite que existan valores negativos.
    # Y se usa int16 en vez de float32 porque se quiere que los valores sean enteros y no tener
    # problemas con la conversión a uint8 de los flotantes. 
    img1 = img1.astype(np.int16)
    img2 = img2.astype(np.int16)

    # Calcular la diferencia entre las imágenes
    diff = img1 - img2

    # Aplicar la función de reescalado elegida
    if rescale_method == 'add':
        # Se suma 255 y se divide por 2, garantizando que los valores estén en el rango [0, 255]
        diff = (diff + 255) / 2  
    elif rescale_method == 'min':
        # Se resta el mínimo de todos los px, haciendo que el valor minimo sea 0, y luego se 
        # escala a 255, multiplicando por la nueva diferencia entre el valor max y el valor min,
        # escalando los valores para que el maximo sea 255, y asi se garantiza que los valores 
        # estén en el rango [0, 255]
        diff = (diff - diff.min()) * (255 / (diff.max() - diff.min()))
    else:
        raise ValueError("El método de reescalado debe ser 'add' o 'min'")

    # Convertir la imagen de vuelta a uint8 para poder mostrarla
    diff = diff.astype(np.uint8)

    return diff

PATH = "../images/"

# Leer las imagenes en escala de grises
img1 = cv2.imread(PATH + "futbol.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(PATH + "chairs.jpg", cv2.IMREAD_GRAYSCALE)

# Redimensionar las imagenes para que tengan el mismo tamaño
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# Aplicar la funcion de resta o diferencia
result = difference(img1, img2)

cv2.imshow("Resultado", result)
cv2.waitKey(0)
cv2.destroyAllWindows()