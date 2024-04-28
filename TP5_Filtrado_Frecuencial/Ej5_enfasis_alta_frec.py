import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui
import filter_enfasis_alta_frec as f_eaf

WINDOW_NAME = 'Filtro de enfasis de alta frecuencia'

# Inicializar cvui
cvui.init(WINDOW_NAME)

PATH = "../images/"
IMAGE = "camaleon.tif"

img = cv2.imread(f"{PATH}{IMAGE}", cv2.IMREAD_GRAYSCALE)

#* Parametros para el filtro de enfasis en alta frecuencia
a = [1]   # a >= 0
b = [2]   # b > a
sigma = [10]   # Desviacion estandar para el filtro gaussiano

while True:
    #* Crear una imagen en blanco para la interfaz de usuario
    frame = np.zeros((300, 500), np.uint8)

    #* Crear un trackbar en la interfaz de usuario
    cvui.text(frame, 50, 20, 'a:')
    cvui.trackbar(frame, 50, 40, 400, a, 1, 200)
    cvui.text(frame, 50, 100, 'b:')
    cvui.trackbar(frame, 50, 120, 400, b, 1, 200)
    cvui.text(frame, 50, 180, 'Sigma:')
    cvui.trackbar(frame, 50, 200, 400, sigma, 1, 200)
    a[0] = int(round(a[0]))  # Redondear el valor de "a"
    b[0] = int(round(b[0]))  # Redondear el valor de "b"
    sigma[0] = int(round(sigma[0]))  # Redondear el valor de D0

    #* TDF
    dft_img = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)    # TDF
    dft_img = np.fft.fftshift(dft_img)   # Centrar la TDF

    #* Crear el filtro de enfasis en alta frecuencia
    mask = f_eaf.filter_enfasis_alta_frec(dft_img, a[0], b[0], sigma[0])

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