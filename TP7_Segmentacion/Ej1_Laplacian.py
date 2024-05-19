"""
Estudie la implementacion del detector de bordes Laplacian (2da. derivada) y
analice su uso variando la talla del filtro.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import cvui
import numpy as np
import edge_detectors as ed

PATH = "../images/"

img = cv2.imread(PATH+'estanbul.tif')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

WINDOW_NAME = 'Laplacian'
CONTROL_WINDOW = 'Settings'
cvui.init(WINDOW_NAME)
cvui.init(CONTROL_WINDOW)

ksize_val = [3]     # Size del kernel

control_frame = np.zeros((150, 250, 3), np.uint8)

while True:
    control_frame[:] = (49, 52, 49)

    cvui.text(control_frame, 10, 40, 'Kernel Size')
    cvui.trackbar(control_frame, 10, 60, 200, ksize_val, 1, 31, 2)

    img_laplacian = ed.laplacian(img, cv2.CV_8U, ksize=int(ksize_val[0]))

    cvui.imshow(WINDOW_NAME, img_laplacian)
    cvui.imshow(CONTROL_WINDOW, control_frame)

    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()