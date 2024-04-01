"""
Al final del proceso de manufactura de placas madres, de marca ASUS modelo
A7V600, se obtienen dos clases de producto final: A7V600-x y A7V600-SE.

Implemente un algoritmo, que a partir de una imagen, determine que tipo de
placa es. Haga uso de las tecnicas de realce aprendidas y utilice las imagenes
a7v600-x.gif y a7v600-SE.gif. 

Adapte el metodo de forma que contemple el reconocimiento de imagenes que han sido afectadas
por un ruido aleatorio impulsivo (a7v600-x(RImpulsivo).gif y a7v600-SE(RImpulsivo).gif ).
"""

#! Pensar en otros metodos usando tecnicas de realce aprendidas, porque este metodo es
#! solo contando la cantidad de px negros y blancos dentro de la zona de interes.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

def placa(img):
    """
    Funcion que determina que tipo de placa es a partir de una imagen.
    """
    # Cuento la cantidad de pixeles negros y blancos en la zona de interes elegida
    num_white = np.sum(img[102:142, 198:241] > 80)  
    num_black = np.sum(img[102:142, 198:241] <= 80)  

    plt.figure()
    plt.imshow(img, cmap='gray')
    plt.show()

    # Si hay mas px negros en la zona de interes elegida es una placa de tipo A7V600-X
    if num_black > num_white:   
        return "A7V600-X"
    else:
        return "A7V600-SE"
    
PATH = "../images/"

# Como las imagenes son .gif, en OpenCV se deben cargar como video
cap = cv2.VideoCapture(PATH + "a7v600-X.gif")
ret, img_X = cap.read()     # img_X sera el primer frame del gif o video
cap.release()

cap = cv2.VideoCapture(PATH + "a7v600-SE.gif")
ret, img_SE = cap.read()
cap.release()

cap = cv2.VideoCapture(PATH + "a7v600-X(RImpulsivo).gif")
ret, img_X_RImpulsivo = cap.read()
cap.release()

cap = cv2.VideoCapture(PATH + "a7v600-SE(RImpulsivo).gif")
ret, img_SE_RImpulsivo = cap.read()
cap.release()

# Convertir a escala de grises
img_X = cv2.cvtColor(img_X, cv2.COLOR_BGR2GRAY)
img_SE = cv2.cvtColor(img_SE, cv2.COLOR_BGR2GRAY)
img_X_RImpulsivo = cv2.cvtColor(img_X_RImpulsivo, cv2.COLOR_BGR2GRAY)
img_SE_RImpulsivo = cv2.cvtColor(img_SE_RImpulsivo, cv2.COLOR_BGR2GRAY)

# Crear mascara binaria en una zona de interes de la placa
# Habia probado usar una mascara y multiplicar la imagen, pero era mas simple contar los
# pixeles en la zona de interes sin la mascara.

# mask = np.zeros_like(img_X)
# mask[102:142, 198:241] = 255    # mask[(y0:y1), (x0:x1)] con "y" fila y "x" columna. No se incluye el y1 ni el x1
#                                 # Es como hacer un rectangulo entre los puntos (y0, x0) y (y1, x1)
# plt.figure()
# plt.imshow(mask, cmap='gray')
# plt.show()

print(placa(img_X))
print(placa(img_X_RImpulsivo))
print(placa(img_SE))    
print(placa(img_SE_RImpulsivo))