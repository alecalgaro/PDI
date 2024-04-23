"""
Construya imagenes binarias de: una linea horizontal, una linea vertical, un
cuadrado centrado, un rectangulo centrado, un circulo.

-¿Que espera ver en las TDF de cada una de estas? 
¿Como estima que estara distribuida la energia?
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Tamaño de la imagen
N = 256

# Linea horizontal
img_line_h = np.zeros((N, N))
img_line_h[N//2, :] = 1

# Linea vertical
img_line_v = np.zeros((N, N))
img_line_v[:, N//2] = 1

# Cuadrado centrado
img_c = np.zeros((N, N))
cv2.rectangle(img_c, (N//4, N//4), (3*N//4, 3*N//4), 1, -1)

# Rectangulo centrado
img_r = np.zeros((N, N))
cv2.rectangle(img_r, (N//4, N//8), (3*N//4, 7*N//8), 1, -1)

# Circulo centrado
img_circ = np.zeros((N, N))
cv2.circle(img_circ, (N//2, N//2), N//4, 1, -1)

# Mostrar todas las imagenes
plt.figure()
plt.subplot(2,3,1)
plt.imshow(img_line_h, cmap='gray')
plt.title('Linea horizontal')
plt.subplot(2,3,2)
plt.imshow(img_line_v, cmap='gray')
plt.title('Linea vertical')
plt.subplot(2,3,3)
plt.imshow(img_c, cmap='gray')
plt.title('Cuadrado')
plt.subplot(2,3,4)
plt.imshow(img_r, cmap='gray')
plt.title('Rectangulo')
plt.subplot(2,3,5)
plt.imshow(img_circ, cmap='gray')
plt.title('Circulo')
# plt.show()

""""
Utilice cada una de las imagenes anteriores para calcular la TDF y visualice.

¿Se cumplieron sus pronosticos respecto de sus deniciones?

Varie las dimensiones y localizacion de los objetos en estas imagenes y repita el analisis.
"""

# En el cuadrado, rectangulo y circulo aplicamos np.abs para quedarnos calcular la magnitud de 
# la TDF obtenida y aplicamos logaritmo para visualizar mejor, ya que sino el pico de (0,0) que
# es la componente de brillo medio, es muy grande y no se veria el resto.

# Como use np.fft.fft2 (de numpy), que devuelve una matriz compleja, para calcular la magnitud
# de la TDF uso np.abs. Si hubiera usado cv2.dft (de OpenCV), que devuelve una matriz de dos
# canales, deberia haber usado cv2.magnitude().

# Calcular la TDF de cada imagen
tdf_line_h = np.fft.fft2(img_line_h)    # TDF de la linea horizontal
tdf_line_h = np.fft.fftshift(tdf_line_h)    # Centrar la TDF

tdf_line_v = np.fft.fft2(img_line_v)    # TDF de la linea vertical
tdf_line_v = np.fft.fftshift(tdf_line_v)    # Centrar la TDF

tdf_c = np.fft.fft2(img_c)    # TDF del cuadrado
tdf_c = np.fft.fftshift(tdf_c)    # Centrar la TDF
tdf_c = np.log(1 + np.abs(tdf_c))

tdf_r = np.fft.fft2(img_r)    # TDF del rectangulo
tdf_r = np.fft.fftshift(tdf_r)    # Centrar la TDF
tdf_r = np.log(1 + np.abs(tdf_r))

tdf_circ = np.fft.fft2(img_circ)    # TDF del circulo
tdf_circ = np.fft.fftshift(tdf_circ)    # Centrar la TDF
tdf_circ = np.log(1 + np.abs(tdf_circ))

# Mostrar las TDF
plt.figure()
plt.subplot(2,3,1)
plt.imshow(np.abs(tdf_line_h), cmap='gray')
plt.title('TDF Linea horizontal')
plt.subplot(2,3,2)
plt.imshow(np.abs(tdf_line_v), cmap='gray')
plt.title('TDF Linea vertical')
plt.subplot(2,3,3)
plt.imshow(np.abs(tdf_c), cmap='gray')
plt.title('TDF Cuadrado')
plt.subplot(2,3,4)
plt.imshow(np.abs(tdf_r), cmap='gray')
plt.title('TDF Rectangulo')
plt.subplot(2,3,5)
plt.imshow(np.abs(tdf_circ), cmap='gray')
plt.title('TDF Circulo')

plt.show()