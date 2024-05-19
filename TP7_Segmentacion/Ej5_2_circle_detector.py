"""
Estudie la implementacion de la TH para circulos cv.HoughCircles.
Utilizando la imagen 'latas.png', realice un programa que:
- Cuente e informe el numero de latas.
- Que informe el numero de latas discriminando en grandes y chicas.

Realice los preprocesamientos que crea necesarios, y puede probar la robustez
de su implementacion rotando la imagen (180 grados).
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

PATH = "../images/"

# Leer imagen original
img = cv2.imread(PATH+'latas.png')
img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
cv2.imshow('Original', img)
cv2.waitKey(0)

# Escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
cv2.imshow('Gray', gray)
cv2.waitKey(0)

# Se aplica un suaavizado a la imagen con un filtro de mediana
# Mientras mas grande el kernel, mas suavizado y mejor deteccion de la circunferencia
# exterior en este caso, ya que las latas tienen otras circunferencias en el centro
gray_blurred = cv2.medianBlur(gray, 27)
cv2.imshow('Blur', gray_blurred )
cv2.waitKey(0)

# Contadores para latas grandes y chicas
count_big = 0
count_small = 0

# Aplicar la tranfromada de Hough para deteccion de circulos (HoughCircles)
# Parametros:
# - imagen luego del pre procesamiento
# - metodo de deteccion a realizar, por lo general se utiliza HOUGH_GRADIENT
# - relacion inversa de la resolucion del acumulador, lo ideal es usar 1 porque se tiene la misma resolucion que la imagen
# - distancia minima (en pixeles) entre el centro y las circunferencias detectadas
# - param1: en el caso de utilizar el metodo HOUGH_GRADIENT, es el umbral maximo en la deteccion de bordes por Canny
# - param2: en el caso de utilizar el metodo HOUGH_GRADIENT, es el umbral minimo en la deteccion de bordes por Canny
# - minRadiu: radio minimo del circulo a detectar
# - maxRadius: radio maximo del circulo a detectar 
detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 40, param1 = 50, param2 = 20, minRadius = 1, maxRadius = 40) 
  
if detected_circles is not None: 
    # Convertir los parametros del circulo (a, b, r) en enteros de 16 bits
    detected_circles = np.uint16(np.around(detected_circles)) 
  
    # Recorrer todos los circulos detectados
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Contar latas grandes y chicas
        if(r > 37):
            count_big += 1
        else:
            count_small += 1

        # Dibujar la circunferencia
        cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
        
        # Mostrar los datos de las circunferencias
        print("Centro ({:}, {:}), radio = {:}".format(a, b, r))
  
        # Dibujar un circulo pequeño alrededor del centro
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
		
        # Mostrar una a una las circunferencias detectadas
        cv2.imshow("Deteccion de circunferencias", img) 
        cv2.waitKey(0) 
        
cv2.destroyAllWindows()

# Mostrar resultados
print("Cantidad total de latas: ", count_big + count_small)
print("Numero de latas grandes: ", count_big)
print("Numero de latas chicas: ", count_small)