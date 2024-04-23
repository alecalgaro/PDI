import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui
import frequency_filters_PA as f_PA

WINDOW_NAME = 'Filtro PA Butterworth'

# Inicializar cvui
cvui.init(WINDOW_NAME)

PATH = "../images/"
IMAGE = "camaleon.tif"

img = cv2.imread(f"{PATH}{IMAGE}", cv2.IMREAD_GRAYSCALE)

#* Parametros para el filtro PA Butterworth
D0 = [50]   # Frecuencia de corte
n = [50]    # Orden del filtro

while True:
    #* Crear una imagen en blanco para la interfaz de usuario
    frame = np.zeros((200, 500), np.uint8)

    #* Crear un trackbar en la interfaz de usuario
    cvui.text(frame, 50, 20, 'Frecuencia de corte (D0):')
    cvui.trackbar(frame, 50, 40, 400, D0, 1, 200)
    cvui.text(frame, 50, 120, 'Orden del filtro (n):')
    cvui.trackbar(frame, 50, 140, 400, n, 1, 100)
    D0[0] = int(round(D0[0]))  # Redondear el valor de D0
    n[0] = int(round(n[0]))  # Redondear el valor de "n"

    #* TDF
    dft_img = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)    # TDF
    dft_img = np.fft.fftshift(dft_img)   # Centrar la TDF

    #* Crear el filtro PA Butterworth
    mask = f_PA.filter_PA_butterworth(dft_img, D0[0], n[0])

    #* Aplicar el filtro
    dft_img *= mask

    #* Realizar la TDF inversa
    dft_ishift = np.fft.ifftshift(dft_img)  # Descentrar
    img_back = cv2.idft(dft_ishift, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)  # TDF inversa
    img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])  # Magnitud
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)  # Normalizar

    #* Mostrar las imagenes
    cv2.imshow(WINDOW_NAME, frame)
    cv2.imshow('Original', img)
    cv2.imshow('Filtrada', img_back)

    #* Salir del bucle si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()