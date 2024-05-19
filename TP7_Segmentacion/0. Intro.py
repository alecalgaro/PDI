"""
En este archivo ire dejando ejemplos sobre las funciones que se recomienda investigar
al comienzo de la practica. 
En el word con anotaciones dejo las explicaciones de cada función con sus parámetros.
"""

PATH = "../images/"

"""
dst = cv.filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]])

Ya la expliqué en otra práctica.
"""

"""
dst = cv.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]])
"""

import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar la operación Sobel
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

# Mostrar las imágenes
cv2.imshow('Original', img)
cv2.imshow('Sobel X', sobelx)
cv2.imshow('Sobel Y', sobely)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
dst = cv.Laplacian(src, ddepth[, dst[, ksize[, scale[, delta[, borderType]]]]])
"""

import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar la operación Laplaciana
laplacian = cv2.Laplacian(img, cv2.CV_64F, ksize=5)

# Mostrar las imágenes
cv2.imshow('Original', img)
cv2.imshow('Laplacian', laplacian)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
edges = cv.Canny(src, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]])
"""

import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar la operación Canny
edges = cv2.Canny(img, 100, 200)

# Mostrar las imágenes
cv2.imshow('Original', img)
cv2.imshow('Edges', edges)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
lines = cv.HoughLines( src, rho, theta, threshold[, lines[, srn[, stn[, min theta[, max theta]]]]])
"""

import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Detectar bordes usando Canny
edges = cv2.Canny(img, 50, 150, apertureSize=3)

# Detectar líneas usando HoughLines
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

# Dibujar las líneas
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Mostrar la imagen
cv2.imshow('Hough Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
lines = cv.HoughLinesP( src, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
"""

import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Detectar bordes usando Canny
edges = cv2.Canny(img, 50, 150, apertureSize=3)

# Detectar segmentos de línea usando HoughLinesP
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

# Dibujar los segmentos de línea
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Mostrar la imagen
cv2.imshow('Hough LinesP', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
circles = cv.HoughCircles( src, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]])
"""

import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Suavizar la imagen
img = cv2.medianBlur(img, 5)

# Detectar círculos usando HoughCircles
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

# Dibujar los círculos
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

# Mostrar la imagen
cv2.imshow('Hough Circles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
retval, labels = cv.connectedComponents( src[, labels[, connectivity[, ltype]]])
"""

import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Binarizar la imagen
_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Etiquetar componentes conectados
retval, labels = cv2.connectedComponents(img)

# Mostrar la imagen de etiquetas
cv2.imshow('Connected Components', labels)
cv2.waitKey(0)
cv2.destroyAllWindows()