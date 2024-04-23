"""
Calcule la TDF de una imagen, obtenga magnitud y fase.

Genere una imagen reconstruida solo con la magnitud considerando fase cero
y genere otra imagen reconstruida usando solo fase de la imagen considerando
magnitud unitaria.

Visualice las imagenes y saque conclusiones sobre el aporte de ambas componentes
a la reconstruccion de la imagen.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

PATH = "../images/"
# IMAGE = "puente.jpg"
IMAGE = "ferrari-c.png"

img = cv2.imread(f"{PATH}{IMAGE}", cv2.IMREAD_GRAYSCALE)

#* TDF
tdf_img = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)    # TDF
tdf_img = np.fft.fftshift(tdf_img)   # Centrar la TDF

#* Separar magnitud y fase
magnitude, phase = cv2.cartToPolar(tdf_img[:,:,0], tdf_img[:,:,1])

#* Generar imagen solo con la magnitud (fase 0)
magnitude_complex = np.zeros_like(tdf_img)
magnitude_complex[:,:,0], magnitude_complex[:,:,1] = cv2.polarToCart(magnitude, np.zeros_like(phase))
dft_ishift = np.fft.ifftshift(magnitude_complex)  # Descentrar
img_back = cv2.idft(dft_ishift, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)  # TDF inversa
img_mag = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])  # Magnitud
img_mag = cv2.log(img_mag + 1)  # Aplicar logaritmo para reducir el rango de valores y que los detalles se vean mejor
img_mag = cv2.normalize(img_mag, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)  # Normalizar después de la transformación logarítmica

#* Generar imagen solo con la fase (magnitud unitaria)
phase_complex = np.zeros_like(tdf_img)
phase_complex[:,:,0], phase_complex[:,:,1] = cv2.polarToCart(np.ones_like(magnitude), phase)
dft_ishift = np.fft.ifftshift(phase_complex)  # Descentrar
img_back = cv2.idft(dft_ishift, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)  # TDF inversa
img_phase = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])  # Magnitud
img_phase = cv2.normalize(img_phase, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

#* Mostrar imagenes
plt.figure()
plt.subplot(1,3,1)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.axis('off')
plt.subplot(1,3,2)
plt.imshow(img_mag, cmap='gray')
plt.title('Solo magnitud')
plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(img_phase, cmap='gray')
plt.title('Solo fase')
plt.axis('off')
plt.show()