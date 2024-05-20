"""
Estudie detalladamente los parametros de la implementacion de Sobel de OpenCV.
Realice un programa que aplique Sobel y le permita variar parametros:
- el tipo de dato del resultado (CV 8U; CV 64F)
- derivadas en x e y (dx, dy)
- el tamano de la mascara (ksize)

Cargue la imagen patron_bordes.jpg y obtenga los siguientes resultados:
- perfiles de intensidad que le permitan intuir los resultados posteriores
- los bordes en direccion x
- los bordes en direccion y
- los bordes en todos los sentidos
- los bordes en todos los sentidos variando ddepth
- los bordes en todos los sentidos variando el parametro ksize (3, 5 y 7)
- los bordes utilizando la apertura de Scharr (ksize = FILTER SCHARR (-1)))
Repita con una imagen real, analice los resultados y comparelos.
"""

import cv2
import cvui
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH = "../images/"

img = cv2.imread(PATH+'estanbul.tif',0)

WINDOW_NAME = 'Sobel'
CONTROL_WINDOW = 'Settings'
cvui.init(WINDOW_NAME)
cvui.init(CONTROL_WINDOW)

ddepth_val = [1]  # 1 (check) -> CV_8U, 0 -> CV_64F
horizontal_val = [0]
vertical_val = [0]
diagonal_val = [0]
all_directions_val = [0]

ksize_val = [1]  # indice para elegir el size del kernel
ksize_values = [-1, 3, 5, 7]  # posibles valores del kernel size

control_frame = np.zeros((400, 400, 3), np.uint8)

while True:
    control_frame[:] = (49, 52, 49)

    cvui.text(control_frame, 10, 20, 'Ddepth (0 for CV_8U, 1 for CV_64F)')
    cvui.checkbox(control_frame, 10, 40, 'Ddepth', ddepth_val)
    cvui.text(control_frame, 10, 90, 'Horizontal edges')
    cvui.checkbox(control_frame, 10, 110, 'Horizontal', horizontal_val)
    cvui.text(control_frame, 10, 150, 'Vertical edges')
    cvui.checkbox(control_frame, 10, 170, 'Vertical', vertical_val)
    cvui.text(control_frame, 10, 210, 'Diagonal edges')
    cvui.checkbox(control_frame, 10, 230, 'Diagonal', diagonal_val)
    cvui.text(control_frame, 10, 270, 'Edges in all directions')
    cvui.checkbox(control_frame, 10, 290, 'All directions', all_directions_val)
    cvui.text(control_frame, 10, 330, 'Kernel Size')
    cvui.trackbar(control_frame, 10, 350, 200, ksize_val, 0, 3)

    # Seteo los valores de los parametros
    ddepth = cv2.CV_8U if ddepth_val[0] else cv2.CV_64F
    ksize = ksize_values[int(ksize_val[0])]

    # Aplico el filtro de Sobel en la direccion elegida
    if horizontal_val[0]:   # horizontal
        img_sobel = cv2.Sobel(img, ddepth, dx=1, dy=0, ksize=ksize)
    elif vertical_val[0]:   # vertical
        img_sobel = cv2.Sobel(img, ddepth, dx=0, dy=1, ksize=ksize)
    elif diagonal_val[0]:   # diagonal
        img_sobel = cv2.Sobel(img, ddepth, dx=1, dy=1, ksize=ksize)
    elif all_directions_val[0]:  # todas las direcciones
        sobelx = cv2.Sobel(img, ddepth, dx=1, dy=0, ksize=ksize)
        sobely = cv2.Sobel(img, ddepth, dx=0, dy=1, ksize=ksize)
        sobeldiag = cv2.Sobel(img, ddepth, dx=1, dy=1, ksize=ksize)
        img_sobel = cv2.add(cv2.add(sobelx, sobely), sobeldiag)
    else:
        img_sobel = img.copy()

    cvui.imshow(WINDOW_NAME, img_sobel)
    cvui.imshow(CONTROL_WINDOW, control_frame)

    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()