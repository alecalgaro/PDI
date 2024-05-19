"""
Implemente un programa que le permita evaluar el comportamiento del detector
de bordes de Canny, mientras varia sus parametros de forma interactiva.
Evalue los resultados al cambiar el parametro L2gradient.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import cvui
import numpy as np

PATH = "../images/"

img = cv2.imread(PATH+'building.jpg',0)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

WINDOW_NAME = 'Canny Edge Detector'
CONTROL_WINDOW = 'Settings'
cvui.init(WINDOW_NAME)
cvui.init(CONTROL_WINDOW)

min_val = [100.0]    # umbral valor minimo (se descartar los gradientes de intensidad menores)
max_val = [200.0]    # umbral valor maximo (se considera como bordes los gradientes de intensidad mayores)
L2 = [False]        # para elegir si se quiere usar L2 gradient

# Si L2gradient es verdadero, encuentra la magnitud del gradiente usando la ecuación 
# sqrt{(dI/dx)^2 + (dI/dy)^2} (L2 norm), que es más exacta. Si es falso, utiliza la 
# ecuación |dI/dx| + |dI/dy| (L1 norm). Es opcional y su valor predeterminado es False.

control_frame = np.zeros((220, 300, 3), np.uint8)

while True:
    control_frame[:] = (49, 52, 49)

    cvui.text(control_frame, 10, 20, 'Min Value')
    cvui.trackbar(control_frame, 10, 40, 250, min_val, 0., 255.)
    cvui.text(control_frame, 10, 90, 'Max Value')
    cvui.trackbar(control_frame, 10, 120, 250, max_val, 0., 255.)
    cvui.checkbox(control_frame, 10, 180, 'Use L2 gradient', L2)

    img_canny = cv2.Canny(img, int(min_val[0]), int(max_val[0]), L2gradient=L2[0])

    cvui.imshow(WINDOW_NAME, img_canny)
    cvui.imshow(CONTROL_WINDOW, control_frame)

    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()