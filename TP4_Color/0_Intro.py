"""
    Antes de comenzar, le recomendamos estudiar el funcionamiento de las siguientes funciones
    de openCV (https://docs.opencv.org/):
    - minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(src[, mask])
    - mv = cv.split( m [, mv])
    o dst = cv.extractChannel(src, coi[, dst])
    - dst = cv.merge( mv [, dst])
    o dst = cv.insertChannel(src, dst, coi)
    - dst = cv.inRange(src, lowerb, upperb[, dst])
    - dst = cv.bitwise_and(src1, src2[, dst[, mask]])

    * OpenCV le provee el modelo HSV, para obtener el canal I, implemente I = (B+G+R)/3
    (el promedio de los tres canales)
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

PATH = "../images/"

"""
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(src[, mask])

La función cv2.minMaxLoc() de OpenCV se utiliza para encontrar el valor mínimo y máximo de los 
píxeles en una imagen en escala de grises, así como la ubicación (loc) de esos valores en la imagen.

La función toma dos argumentos:

src: La imagen de entrada. Debe ser una imagen en escala de grises (una matriz 2D).
mask (opcional): Una máscara de la misma dimensión que src. Sirve para considerar solo los píxeles 
de src (la imagen) donde la máscara es no nula.

La función devuelve cuatro valores:

- minVal: El valor mínimo de los píxeles en la imagen (o en la máscara, si se proporciona).
- maxVal: El valor máximo de los píxeles en la imagen (o en la máscara, si se proporciona).
- minLoc: Una tupla (x, y) que representa la ubicación del valor mínimo en la imagen.
- maxLoc: Una tupla (x, y) que representa la ubicación del valor máximo en la imagen.

Ejemplo de cómo se podría usar esta función:
"""

img = cv2.imread(PATH + "cameraman.tif", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Imagen", img)

# Encuentra el valor mínimo y máximo y sus ubicaciones
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(img)

print(f"Valor minimo: {minVal} en la ubicacion {minLoc}")
print(f"Valor maximo: {maxVal} en la ubicacion {maxLoc}")

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
mv = cv.split( m [, mv])

La función cv.split() de OpenCV se utiliza para dividir una imagen multicanal en varios canales 
de imagen de un solo canal.

Parámetros:

- m: La imagen de entrada. Debe ser de 8 bits, 16 bits, 32 bits de profundidad y puede tener 
cualquier número de canales.
- mv: El vector de salida de imágenes de un solo canal. El número de canales se determinará 
automáticamente por el número de canales en la imagen de entrada.
Por ejemplo, si tienes una imagen en color en formato BGR (Blue, Green, Red), puedes usar 
cv.split() para dividirla en sus tres canales de color individuales.

Ejemplo de cómo usar cv.split():
"""

# Cargar una imagen en color
img = cv2.imread(PATH + 'futbol.jpg')

# Dividir la imagen en los canales B, G y R
b, g, r = cv2.split(img)

# Ahora b, g y r son matrices que representan los canales azul, verde y rojo de la imagen

# Importante:
# OpenCV lee las imagenes en formato BGR, si yo convierto una imagen a RGB u otro modelo de color,
# cv2.split() dividira los canalas de acuerdo al espacio de color de la imagen. Por ejemplo:

# Convertir la imagen de BGR a RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# Dividir la imagen en los canales R, G y B
r, g, b = cv2.split(img_rgb)

# Convertir la imagen de BGR a HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# Dividir la imagen en los canales H, S y V
h, s, v = cv2.split(img_hsv)

"""
dst = cv.extractChannel(src, coi[, dst])

La función cv.extractChannel() de OpenCV se utiliza para extraer un canal específico de una imagen 
multicanal.

Parámetros:
- src: La imagen de entrada. Debe ser de 8 bits, 16 bits, 32 bits de profundidad y puede tener 
cualquier número de canales.
- coi: El índice del canal a extraer. Los índices de los canales comienzan desde 0. Por ejemplo, 
para una imagen en formato BGR, 0 sería azul, 1 sería verde y 2 sería rojo.
- dst: La imagen de salida de un solo canal. Este es un parámetro opcional.

Ejemplo de uso:
"""

# Cargar una imagen en color (en formato BGR)
img = cv2.imread(PATH + 'futbol.jpg')

# Extraer el canal rojo (rojo -> indice 2)
red_channel = cv2.extractChannel(img, 2)
# Ahora red_channel es una matriz que representa el canal rojo de la imagen.

"""
dst = cv.merge( mv [, dst])

La función cv.merge() de OpenCV se utiliza para combinar varios canales de imagen de un solo canal 
en una imagen multicanal.

Parámetros:
- mv: Un vector de imágenes de un solo canal. El número de canales en la imagen de salida se 
determinará automáticamente por el número de imágenes en este vector.
- dst: La imagen de salida multicanal. Este es un parámetro opcional.

Por ejemplo, si se tiene tres canales de imagen de un solo canal que representan los canales 
B, G y R de una imagen, se puede usar cv.merge() para combinarlos en una imagen en color.

Ejemplo de cómo usar cv.merge():
"""

# Cargar una imagen en color
img = cv2.imread(PATH + 'futbol.jpg')

# Dividir la imagen en los canales B, G y R
b, g, r = cv2.split(img)

# Combinar los canales B, G y R en una imagen en color
merged_img = cv2.merge([b, g, r])
# Ahora merged_img es una imagen en color que se ha combinado a partir de los canales B, G y R.

cv2.imshow("Imagen", merged_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
dst = cv.insertChannel(src, dst, coi)

La función cv.insertChannel(src, dst, coi) de OpenCV es utilizada para insertar un canal de una 
imagen en otra imagen.

Parámetros:
- src: Es la imagen fuente. Es el canal que se quiere insertar en la imagen de destino.
- dst: Es la imagen de destino. Es la imagen en la que se quiere insertar el canal.
- coi: Es el índice del canal de salida. Es el índice del canal en la imagen de destino donde 
se quiere insertar el canal de la imagen fuente.

La función toma un canal de la imagen fuente (src) y lo inserta en la imagen de destino (dst) 
en el índice de canal especificado (coi). El resultado es almacenado en dst.

Esta función puede no estar disponible en todas las versiones de OpenCV. En algunas versiones, 
puede ser necesario usar una combinación de otras funciones para lograr el mismo resultado.

Ejemplo de uso de cv.insertChannel():
"""

# Github copilot me decia que esta funcion no existe en OpenCV pero que la podia reemplazar usando
# la funcion cv2.split() y cv2.merge() de la siguiente manera:

# Cargar una imagen en color
img = cv2.imread(PATH + 'futbol.jpg')

# Dividir la imagen en canales B, G, R
b, g, r = cv2.split(img)

# Crear una matriz de ceros del mismo tamaño que uno de los canales
zero_channel = np.zeros_like(b)

# Insertar el canal de ceros en el lugar del canal verde (G)
merged = cv2.merge((b, zero_channel, r))

# Guardar la imagen resultante (sera una imagen con el canal verde eliminado)
cv2.imwrite('images_intro/image_with_zero_green.jpg', merged)

cv2.imshow("Imagen merged (sin color verde)", merged)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
dst = cv.inRange(src, lowerb, upperb[, dst])

La función cv2.inRange(src, lowerb, upperb[, dst]) de OpenCV se utiliza para comprobar si los 
elementos de la matriz de la imagen de origen (src) se encuentran dentro del rango definido por 
los límites inferior (lowerb) y superior (upperb).

Parámetros:
- src: Es la imagen de origen.
- lowerb: Es el límite inferior del rango.
- upperb: Es el límite superior del rango.
- dst (opcional): Es la imagen de destino.

La función devuelve una imagen binaria, donde los píxeles de la imagen de origen que caen dentro 
del rango se establecen en 255 (blanco), y los que caen fuera del rango se establecen en 0 (negro).

Ejemplo de cómo se puede utilizar esta función para filtrar un color específico en una imagen:
"""

# Cargar una imagen en color
img = cv2.imread(PATH + 'futbol.jpg')

# Definir el rango de color para el filtrado
# Recordar que es [B, G, R]. 
# Ese rango filtra los colores predominantemente rojos, con un poco de mezcla de azul y verde.
lowerb = np.array([0, 0, 100])  # Rojo inferior
upperb = np.array([60, 60, 255])  # Rojo superior

# Aplicar la función inRange.
# Crea una máscara donde los píxeles que caen dentro del rango de color se establecen 
# en blanco y los que caen fuera del rango se establecen en negro. 
mask = cv2.inRange(img, lowerb, upperb)

# Guardar la imagen resultante
cv2.imwrite('images_intro/image_in_range.jpg', mask)

# Al mostrar la imagen vemos que filtra la camiseta del arbitro que es roja, entonces esa parte
# queda en blanco y todo el resto en negro. Se puede ir probando cambiar el rango (lowerb y upperb).
cv2.imshow("Imagen filtrada", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
dst = cv.bitwise_and(src1, src2[, dst[, mask]])

La función cv.bitwise_and(src1, src2[, dst[, mask]]) de OpenCV se utiliza para realizar una 
operación AND a nivel de bit entre dos imágenes (o entre una imagen y un escalar).

Parámetros:
- src1: Primera imagen de origen.
- src2: Segunda imagen de origen.
- dst (opcional): Imagen de destino.
- mask (opcional): Máscara de operación opcional. Si la matriz de máscara es no vacía, debe tener 
el mismo tamaño que src1 o src2, y su tipo debe ser CV_8U.

La operación AND a nivel de bit compara cada bit de src1 con el bit correspondiente de src2: si 
ambos bits son 1, el bit correspondiente en la salida es 1, de lo contrario es 0.

Ejemplo de cómo se puede utilizar esta función para aplicar una máscara a una imagen:

En este ejemplo, cargamos una imagen y creamos una máscara binaria con una región blanca (255) en 
una ubicación específica. Luego, aplicamos la función cv.bitwise_and() para aplicar la máscara a 
la imagen: solo los píxeles de la imagen que corresponden a los píxeles blancos de la máscara se 
mantienen, el resto se pone a negro. Finalmente, guardamos la imagen resultante.

Un uso de esta función es para quedarnos con una parte de interés de una imagen o video. En el
video que dejo abajo lo usan para crear un sistema de detección de movimiento usando un video y
quedándose solo con el sector de interes donde se quiere detectar:
https://www.youtube.com/watch?v=-MJ435F5VIE&t=322s
"""

# Cargar una imagen en color
img = cv2.imread(PATH + 'futbol.jpg')

# Crear una máscara binaria
# Se usa img.shape[:2] porque img es a color asi que tengo (rows, colw, 3) y para la mascara 
# solo necesito (rows, cols) asi que con [:2] me quedo con los dos primeros elementos
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:400] = 255

# Aplicar la función bitwise_and
masked_img = cv2.bitwise_and(img, img, mask=mask)

# Guardar la imagen resultante
cv2.imwrite('images_intro/image_masked.jpg', masked_img)

cv2.imshow("Bitwise_and", masked_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
