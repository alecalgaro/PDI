"""
    Ejercicio 2: Informacion de intensidad.
    1. Informe los valores de intensidad de puntos particulares de la imagen 
    (opcional: determine la posicion en base al click del mouse).
"""

"""
    Tener en cuenta:
    En PDI "intensidad" se refiere a la luminosidad o el valor de brillo de un píxel en la imagen. 
    En una imagen en escala de grises, la intensidad de un píxel se representa como un valor 
    único que va de 0 (negro) a 255 (blanco). En una imagen a color, la intensidad puede referirse 
    a la luminosidad en un modelo de color específico, como el modelo de color HSV 
    (Hue, Saturation, Value), donde "Value" representa la intensidad.

    Para obtener un único valor de intensidad de un px en una imagen a color, se puede convertir
    la imagen a escala de grises.
    En caso de necesitar trabajar con la imagen en color y querer obtener un valor de intensidad, 
    una opción es convertir la imagen del espacio de color BGR al espacio de color HSV y usar el 
    componente V (Value) como la intensidad. Sin embargo, este valor de intensidad no será 
    exactamente el mismo que el que obtendrías de una imagen en escala de grises, ya que el modelo 
    de color HSV tiene en cuenta tanto el color como el brillo.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2

PATH = "../images/"

# Cargar imagen en escala de grises
img = cv2.imread(PATH + "camino.tif", cv2.IMREAD_GRAYSCALE)

# Obtener valores de intensidad de px particulares
print("")
print('Intensidad de puntos particulares:')
print('Punto (0, 0): ', img[0, 0])
print('Punto (100, 100): ', img[100, 100])

# Obtener los valores de intensidad a partir del click del mouse
def obtener_intensidad(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Punto (', x, ', ', y, '): ', img[y, x])

print('Intensidad de puntos a partir del click del mouse:')
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen', obtener_intensidad)

# Muestro la imagen
cv2.imshow('Imagen', img)   # mismo nombre que la ventana creada
cv2.waitKey(0)
cv2.destroyAllWindows()
