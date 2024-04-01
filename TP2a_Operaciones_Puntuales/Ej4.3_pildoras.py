"""
En una fabrica de medicamentos se desea implementar un sistema para la inspeccion visual 
automatica de blisters en la linea de empaquetado. La adquisicion de la imagen se realiza 
en escala de grises mediante una camara CCD fija y bajo condiciones controladas de iluminacion, 
escala y enfoque. 
El objetivo consiste en determinar en cada instante si el blister que esta siendo analizado se 
encuentra incompleto, en cuyo caso la region correspondiente a la pildora faltante presenta una 
intensidad similar al fondo. 

Escriba una funcion que reciba como parametro la imagen del blister a analizar y devuelva un 
mensaje indicando si el mismo contiene o no la totalidad de las pildoras.
En caso de estar incompleto, indique la posicion (x,y) de las pildoras faltantes. 
Verifique el funcionamiento con las imagenes "blister_completo.jpg" y "blister_incompleto.jpg".
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

PATH = "../images/"

def isBlisterComplete(img):
    """
    Funcion que recibe una imagen de un blister de pildoras y determina si un blister esta 
    completo o incompleto e indica las posiciones de pildoras faltantes.
    """
    # Creo una mascara binaria con las pildoras (fondo blanco y pildoras negras)
    mask = img < 100

    # cv2.imshow("mask", mask.astype(np.uint8) * 255)
    plt.figure()
    plt.imshow(mask, cmap="gray")
    plt.show()

    # Posiciones de las pildoras en el blister (posiciones [y, x])
    positions = [[50,50], [50,100], [50,150], [50,200], [50,250],
             [100,50], [100,100], [100,150], [100,200], [100,250]]

    missing_pills = []  # Lista para guardar las posiciones de las pildoras faltantes
    
    # Recorro las posiciones de las pildoras y si alguna no esta en la mascara (!=0), la agrego a la lista
    for pos in positions:
        if mask[pos[0], pos[1]] != 0:
            missing_pills.append(pos)
            cv2.rectangle(img, (pos[1]-10, pos[0]-10), (pos[1]+10, pos[0]+10), (255, 0, 0), 1) 

    # Muestro la imagen del blister con rectangulos en las pildoras faltantes
    cv2.imshow('Blister', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if missing_pills:
        return "Blister incompleto. Faltan pildoras en las posiciones: " + str(missing_pills)
    else:
        return "Blister completo"

#* Cargo las imagenes de prueba
img_completo = cv2.imread(PATH + "blister_completo.jpg", cv2.IMREAD_GRAYSCALE)
img_incompleto = cv2.imread(PATH + "blister_incompleto.jpg", cv2.IMREAD_GRAYSCALE)

print(isBlisterComplete(img_completo))
print(isBlisterComplete(img_incompleto))