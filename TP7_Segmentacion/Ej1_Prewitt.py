"""
Deteccion de bordes.

Implemente el detector de bordes de Prewitt en una funcion que retorne una
imagen binaria con los bordes detectados.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import matplotlib.pyplot as plt

import edge_detectors as ed

PATH = "../images/"

img = cv2.imread(PATH+'patron_bordes.jpg',0)

#* Detector de bordes de Prewitt
img_prewitt = ed.prewitt(img)

plt.figure(figsize=(10,5))
plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.subplot(122)
plt.imshow(img_prewitt, cmap='gray')
plt.title('Prewitt')
plt.show()