import cv2
import numpy as np
import color_slicing as cs
import cvui


"""
Segmentacion de color en HSV utilizando la webcam.
"""

# Abrir la webcam (0)
video = cv2.VideoCapture(0)

WINDOW_NAME = 'Video segmentado'
WINDOW_NAME_CONTROLS = 'Controles'
cvui.init(WINDOW_NAME)
cvui.init(WINDOW_NAME_CONTROLS)

UI = np.zeros((580, 350, 3), np.uint8)

# Valores iniciales para los trackbars
h_min = [0]
s_min = [0]
v_min = [0]
h_max = [179]
s_max = [255]
v_max = [255]

while True:
    UI[:] = (49, 52, 49)

    # Crear los trackbars para los valores mínimos y máximos de cada canal de color en HSV
    cvui.text(UI, 10, 30, 'H min')
    cvui.trackbar(UI, 10, 50, 300, h_min, 0, 179)
    cvui.text(UI, 10, 120, 'H max')
    cvui.trackbar(UI, 10, 140, 300, h_max, 0, 179)
    cvui.text(UI, 10, 210, 'S min')
    cvui.trackbar(UI, 10, 230, 300, s_min, 0, 255)
    cvui.text(UI, 10, 300, 'S max')
    cvui.trackbar(UI, 10, 320, 300, s_max, 0, 255)
    cvui.text(UI, 10, 380, 'V min')
    cvui.trackbar(UI, 10, 400, 300, v_min, 0, 255)
    cvui.text(UI, 10, 470, 'V max')
    cvui.trackbar(UI, 10, 490, 300, v_max, 0, 255)

    # Crear los arrays lower y upper
    lower = np.array([h_min[0], s_min[0], v_min[0]])
    upper = np.array([h_max[0], s_max[0], v_max[0]])

    # Leer el siguiente fotograma del video
    ret, frame = video.read()

    # Si el fotograma no se leyó correctamente, salir del bucle
    if not ret:
        break

    # Aplicar el rebanado de color (el fotograma se convierte a HSV en la funcion)
    frame_slicing = cs.color_slicing_hsv(frame, lower, upper)

    # Mostrar el fotograma filtrado y los controles
    cvui.imshow(WINDOW_NAME_CONTROLS, UI)
    cvui.imshow(WINDOW_NAME, frame_slicing)

    # Salir del bucle si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

video.release()
cv2.destroyAllWindows()