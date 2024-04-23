"""
Reproduzca el experimento de Openheim utilizando las imagenes "puente.jpg"
y "ferrari-c.png". 
Visualice y comente los resultados.

El experimento de Openheim consiste en combinar la magnitud de una imagen con la fase de otra.
Para ello se deben seguir los siguientes pasos:
1. Aplicar la TDF a ambas imagenes.
2. Separar la magnitud y la fase de cada imagen.
3. Generar una nueva imagen con la magnitud de una imagen y la fase de la otra.
4. Aplicar la TDF inversa a la nueva imagen.

En la imagen resultante se deberia ver que se recuperan los bordes de la imagen que se uso su fase,
pero con distintas magnitud (modulo) porque se uso la magnitud de la otra imagen.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

PATH = "../images/"
IMAGE1 = "puente.jpg"
IMAGE2 = "ferrari-c.png"

img1 = cv2.imread(f"{PATH}{IMAGE1}", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(f"{PATH}{IMAGE2}", cv2.IMREAD_GRAYSCALE)

#* TDF
tdf_img1 = cv2.dft(np.float32(img1), flags=cv2.DFT_COMPLEX_OUTPUT)    # TDF
tdf_img1 = np.fft.fftshift(tdf_img1)   # Centrar la TDF

tdf_img2 = cv2.dft(np.float32(img2), flags=cv2.DFT_COMPLEX_OUTPUT)
tdf_img2 = np.fft.fftshift(tdf_img2)  

#* Separar magnitud y fase
magnitude1, phase1 = cv2.cartToPolar(tdf_img1[:,:,0], tdf_img1[:,:,1])
magnitude2, phase2 = cv2.cartToPolar(tdf_img2[:,:,0], tdf_img2[:,:,1])

#* Imagen con magnitud de img1 y fase de img2
# En polarToCart se combina la magnitud de img1 y fase de img2
magnitude_complex1 = np.zeros_like(tdf_img1)
magnitude_complex1[:,:,0], magnitude_complex1[:,:,1] = cv2.polarToCart(magnitude1, phase2)
dft_ishift = np.fft.ifftshift(magnitude_complex1)  # Descentrar
img_back = cv2.idft(dft_ishift, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)  # TDF inversa
img1_mag2_pha1 = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])  # Magnitud
img1_mag2_pha1 = cv2.normalize(img1_mag2_pha1, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

#* Imagen con magnitud de img2 y fase de img1
# En polarToCart se combina la magnitud de img2 y fase de img1
magnitude_complex2 = np.zeros_like(tdf_img2)
magnitude_complex2[:,:,0], magnitude_complex2[:,:,1] = cv2.polarToCart(magnitude2, phase1)
dft_ishift = np.fft.ifftshift(magnitude_complex2)  # Descentrar
img_back = cv2.idft(dft_ishift, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)  # TDF inversa
img2_mag1_pha2 = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])  # Magnitud
img2_mag1_pha2 = cv2.normalize(img2_mag1_pha2, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

#* Mostrar imagenes
plt.figure()
plt.subplot(1,2,1)
plt.imshow(img1_mag2_pha1, cmap='gray')
plt.title('Magnitud img1 y fase img2')
plt.axis('off')
plt.subplot(1,2,2)
plt.imshow(img2_mag1_pha2, cmap='gray')
plt.title('Magnitud img2 y fase img1')
plt.axis('off')
plt.show()