# Tools for drawing and visualization

import cv2

# Algunas de las funciones que nos permiten dibujar 
# (linea, circulo y rectangulo) en una imagen son:

# cv2.line(imagen, start_point, end_point, color, thickness, line_type)
# thickness = grosor de la linea, line_type = tipo de linea (hay algunas), si no se colocan usan los valores por defecto

# cv2.circle(imagen, center_point, radius, color, thickness, line_type)
# cv2.rectangle(imagen, start_point, end_point, color, thickness)

# cv2.line(image, (0, 0), (100, 100), (255, 0, 0), 5)
# cv2.circle(image, (150, 150), 50, (0, 255, 0), 3)
# cv2.rectangle(image, (200, 200), (300, 300), (0, 0, 255), 2)

# En el proximo archivo mostramos las imagenes con las figuras dibujadas
# utilizando matplotlib.pyplot