import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import argparse
import color_slicing as cs
import cvui

"""
Segmentacion de color en video utilizando modelo de color RGB.
"""

# Si lo quiero usar desde consola:
# python Ej5_segmentacion_RGB_video.py -vi "nombreVideo.mp4"

PATH = '../images/'

default_video = "pedestrians.mp4"

ap = argparse.ArgumentParser() 
ap.add_argument("-vi", "--video", required=False, help="path del video a utilizar")
args = vars(ap.parse_args())

nombre_video = args["video"] if args["video"] else default_video

# Abrir el video
video = cv2.VideoCapture(PATH + nombre_video)

WINDOW_NAME = 'Video segmentado'
WINDOW_NAME_CONTROLS = 'Controles'
cvui.init(WINDOW_NAME)
cvui.init(WINDOW_NAME_CONTROLS)

UI = np.zeros((580, 350, 3), np.uint8)

# Valores iniciales para los trackbars
r_min = [0]
g_min = [0]
b_min = [0]
r_max = [255]
g_max = [255]
b_max = [255]

while True:
    UI[:] = (49, 52, 49)

    # Crear los trackbars para los valores mínimos y máximos de cada canal de color en RGB
    cvui.text(UI, 10, 30, 'R min')
    cvui.trackbar(UI, 10, 50, 300, r_min, 0, 255)
    cvui.text(UI, 10, 120, 'R max')
    cvui.trackbar(UI, 10, 140, 300, r_max, 0, 255)
    cvui.text(UI, 10, 210, 'G min')
    cvui.trackbar(UI, 10, 230, 300, g_min, 0, 255)
    cvui.text(UI, 10, 300, 'G max')
    cvui.trackbar(UI, 10, 320, 300, g_max, 0, 255)
    cvui.text(UI, 10, 380, 'B min')
    cvui.trackbar(UI, 10, 400, 300, b_min, 0, 255)
    cvui.text(UI, 10, 470, 'B max')
    cvui.trackbar(UI, 10, 490, 300, b_max, 0, 255)

    # Crear los arrays lower y upper
    lower = np.array([b_min[0], g_min[0], r_min[0]])
    upper = np.array([b_max[0], g_max[0], r_max[0]])

    # Leer el siguiente fotograma del video
    ret, frame = video.read()

    # Si el fotograma no se leyó correctamente (si no hay mas fotogramas), volver al primer 
    # fotograma para que cuando termine el video se vuelva a repetir
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Aplicar el rebanado de color (el fotograma se convierte a RGB en la funcion)
    frame_slicing = cs.color_slicing_rgb(frame, lower, upper)

    # Mostrar el fotograma filtrado y los controles
    cvui.imshow(WINDOW_NAME_CONTROLS, UI)
    cvui.imshow(WINDOW_NAME, frame_slicing)

    # Salir del bucle si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

video.release()
cv2.destroyAllWindows()