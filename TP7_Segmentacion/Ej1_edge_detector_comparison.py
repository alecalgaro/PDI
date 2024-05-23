"""
Cargue la imagen 'mosquito.jpg' y genere versiones con ruido impulsivo unimodal
(variando el gris en que aparece) y con ruido gaussiano (mu = 0) para
distintos valores de desvio estandar.

Aplique los distintos detectores de bordes a cada caso y compare los desempenos.

Algunas preguntas de guia: 
- En que zonas (debido a que) funciona mejor y en cuales no?
- Que sucede con el ruido?
- Con que tipo de imagenes sacaria mejor provecho de los metodos? 
- Que tipo de preprocesamientos, de los que ya conoce, se le ocurren 
que seran utiles?, etc.
"""

import cv2
import numpy as np
import cvui
import add_impulsive_noise as noise_imp
import add_gaussian_noise as noise_gauss
import edge_detectors as ed
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#* Funcion para aplicar los detectores de bordes
def apply_edge_detectors(img):
    img_prewitt = ed.prewitt(img)
    img_canny = cv2.Canny(img, 100, 200, L2gradient=False)
    img_laplacian = cv2.Laplacian(img, cv2.CV_64F)
    img_sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    img_sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1)
    img_sobel = np.sqrt(img_sobel_x**2 + img_sobel_y**2)
    img_sobel = np.clip(img_sobel, 0, 255).astype(np.uint8)
    return img_prewitt, img_canny, img_laplacian, img_sobel

# Inicializar la ventana de OpenCV y cvui
WINDOW_NAME = 'Noise Control'
cvui.init(WINDOW_NAME)

#* Inicializar las variables de estado (checkboxes y trackbars)
impulsive_noise = [True]
gaussian_noise = [False]
impulsive_param = [0.05]
gaussian_param = [10]

#* Almacenar los valores anteriores de los parametros
prev_impulsive_param = impulsive_param[0]
prev_gaussian_param = gaussian_param[0]

#* Cargar imagen
img = cv2.imread('../images/mosquito.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Original', img)

#* Bucle principal
while True:
    # Frame para mostrar los controles
    frame = np.zeros((200, 300), np.uint8)

    # Dibujar los checkboxes y los trackbars
    cvui.checkbox(frame, 10, 10, 'Impulsive noise', impulsive_noise)
    cvui.trackbar(frame, 10, 40, 200, impulsive_param, 0., 1., 0.01, '%.2f')
    cvui.checkbox(frame, 10, 110, 'Gaussian noise', gaussian_noise)
    cvui.trackbar(frame, 10, 140, 200, gaussian_param, 0., 50., 1, '%.2f')

    # Actualizar la imagen con ruido solo si los parametros (checkboxes y trackbars) cambiaron
    if impulsive_noise[0] and impulsive_param[0] != prev_impulsive_param:
        img_noised = noise_imp.add_impulsive_noise(img, impulsive_param[0], 'unimodal', True)
        prev_impulsive_param = impulsive_param[0]
        
        # Aplicar detectores de bordes
        img_prewitt, img_canny, img_laplacian, img_sobel = apply_edge_detectors(img_noised)
        
        # Mostrar imagenes
        cv2.imshow('Noised', img_noised)    # imagen original con ruido
        cv2.imshow('Prewwit', img_prewitt)
        cv2.imshow('Canny', img_canny)
        cv2.imshow('Laplacian', img_laplacian)
        cv2.imshow('Sobel', img_sobel)

    if gaussian_noise[0] and gaussian_param[0] != prev_gaussian_param:
        img_noised = noise_gauss.add_gaussian_noise(img, gaussian_param[0])
        prev_gaussian_param = gaussian_param[0]
        
        # Aplicar detectores de bordes
        img_prewitt, img_canny, img_laplacian, img_sobel = apply_edge_detectors(img_noised)
        
        # Mostrar imagenes
        cv2.imshow('Noised', img_noised)    # imagen original con ruido
        cv2.imshow('Prewwit', img_prewitt)
        cv2.imshow('Canny', img_canny)
        cv2.imshow('Laplacian', img_laplacian)
        cv2.imshow('Sobel', img_sobel)
    
    # Mostrar controles
    cvui.imshow(WINDOW_NAME, frame)

    # Terminar el bucle si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()