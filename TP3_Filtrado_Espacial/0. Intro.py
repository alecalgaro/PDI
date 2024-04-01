import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import cv2
import numpy as np

PATH = "../images/"

"""
En este archivo habra ejemplos de uso de las funciones que recomienda 
investigar al inicio de la practica.
En el word con anotaciones se dejan explicaciones de cada una, para que sirven 
y cuales son los parametros.
"""

"""
---------- filter2D ----------
dst = cv.filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]])
"""
src = cv2.imread(PATH + 'cameraman.tif')

# Crear un kernel de desenfoque o suavizado de 5x5
# Seria 1/N^2 * np.ones((N,N))
kernel = np.ones((5,5),np.float32)/25

# Otros tipos de kernel explicados en la teoria
# suma 1 -> realce de altas frecuencias (bordes) sin eliminar las bajas (zonas homogeneas)
mask = np.matrix([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
# suma 0 -> realce de altas frecuencias (bordes) eliminando las bajas (zonas homogeneas)
mask = np.matrix([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
# kernel = np.matrix([[0, 1, 0],[1,4,1],[0,1,0]])*(1/8)
# kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])  # para deteccion de bordes

# Aplicar el filtro
dst = cv2.filter2D(src,-1,kernel)

# Mostrar la imagen original y la imagen desenfocada
cv2.imshow('Original', src)
cv2.imshow('Blurred', dst)

# Encontre este ejemplo sobre el parametro borderType de filter2D:
# El abcdefgh del centro seria la imagen y hacia los lados los tipos de bordes.
# cv2.BORDER_CONSTANT,value=1   -- iiiiii|abcdefgh|iiiiii
# cv2.BORDER_REFLECT            -- fedcba|abcdefgh|hgfedcb
# cv2.BORDER_REFLECT_101        -- gfedcb|abcdefgh|gfedcba
# cv2.BORDER_WRAP               -- cdefgh|abcdefgh|abcdefg
# cv2.BORDER_REPLICATE          -- aaaaaa|abcdefgh|hhhhhhh

"""
---------- copyMakeBorder ----------
dst = cv.copyMakeBorder(src, top, bottom, left, right, borderType[, dst[,value]])
"""

src = cv2.imread(PATH + 'cameraman.tif')

# Crear un borde constante de 10 pixeles de color azul ([255, 0, 0] en BGR)
dst = cv2.copyMakeBorder(src, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 0, 0])

# Mostrar la imagen original y la imagen con borde
cv2.imshow('Original', src)
cv2.imshow('Bordered', dst)

"""
---------- getGaussianKernel ----------
kernel Gauss = cv.getGaussianKernel(ksize, sigma[, ktype])
"""

src = cv2.imread(PATH + 'cameraman.tif')

# Generar un kernel gaussiano de tamaño 5.
# La desviacion estandar es 0, por lo que se calcula automaticamente a partir del tamaño del kernel.
gauss_kernel = cv2.getGaussianKernel(5, 0)
print(gauss_kernel)

# Para usar este kernel para suavizar una imagen, se debe convertirlo a un kernel
# bidimensional (2D) multiplicando el kernel por su transpuesta, y luego aplicar
# el filtro con filter2D.

# Convertir el kernel a 2D
gauss_kernel = gauss_kernel @ gauss_kernel.transpose()
# print(gauss_kernel)

# Aplicar el filtro
dst = cv2.filter2D(src, -1, gauss_kernel)

# Mostrar la imagen original y la imagen filtrada
cv2.imshow('Original', src)
cv2.imshow('Filtered', dst)

"""
---------- blur ----------
dst = cv.blur(src, ksize[, dst[, anchor[, borderType]]])
"""

src = cv2.imread(PATH + 'cameraman.tif')

# Aplicar el filtro de desenfoque o suavizado de 5x5
dst = cv2.blur(src, (5, 5))

# Mostrar la imagen original y la imagen desenfocada
cv2.imshow('Original', src)
cv2.imshow('Blurred con cv2.blur', dst)

"""
---------- boxFilter ----------
dst = cv.boxFilter(src, ddepth, ksize[, dst[, anchor[, normalize[,borderType]]]])
"""

src = cv2.imread(PATH + 'cameraman.tif')

# Aplicar el filtro de caja con tamaño de 5x5
dst = cv2.boxFilter(src, -1, (5, 5))

# Mostrar la imagen original y la imagen filtrada
cv2.imshow('Original', src)
cv2.imshow('Box Filter', dst)

"""
---------- GaussianBlur ----------
dst = cv.GaussianBlur(src, ksize, sigmaX[, dst[, sigmaY[, borderType]]])
"""

src = cv2.imread(PATH + 'cameraman.tif')

# Aplicar el filtro gaussiano de 5x5 y desviacion estandar 0
dst = cv2.GaussianBlur(src, (5, 5), 0)

# Mostrar la imagen original y la imagen desenfocada
cv2.imshow('Original', src)
cv2.imshow('Gaussian Blur', dst)

"""
---------- medianBlur ----------
dst = cv.medianBlur(src, ksize[, dst])
"""

# El filtro de mediana es particularmente efectivo para eliminar el ruido de sal y pimienta, 
# ya que reemplaza cada píxel por la mediana de los píxeles en su vecindario.

src = cv2.imread(PATH + 'cameraman.tif')

# Aplicar el filtro de mediana con tamaño de 5
dst = cv2.medianBlur(src, 5)

# Mostrar la imagen original y la imagen desenfocada
cv2.imshow('Original', src)
cv2.imshow('Median Blur', dst)

"""
---------- bilateralFilter ----------
dst = cv.bilateralFilter(src, d, sigmaColor, sigmaSpace[, dst[, borderType]])
"""

src = cv2.imread(PATH + 'cameraman.tif')

# Aplicar el filtro bilateral con un diametro de 9, sigmaColor de 75 y sigmaSpace de 75
dst = cv2.bilateralFilter(src, 9, 75, 75)

# Mostrar la imagen original y la imagen filtrada
cv2.imshow('Original', src)
cv2.imshow('Bilateral Filter', dst)

#* -----------------------------------
cv2.waitKey(0)
cv2.destroyAllWindows()