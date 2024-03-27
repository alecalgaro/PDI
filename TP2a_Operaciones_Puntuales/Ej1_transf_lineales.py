import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui

"""
Una LUT es un vector (o una "tabla") que mapea (reemplaza) un conjunto de valores de entrada 
(los valores de los px de la imagen original) a un conjunto de valores de salida (imagen de salida).
Puede haber distintos tipos de transformaciones: 'Linear', 'Log', 'Threshold'

En la ecuacion general s = ar + c, "r" es el valor de entrada, "a" es el factor de ganancia y "c" 
es el offset. Esta todo explicado en la teoria.
- Con "c" se cambia el brillo general de la imagen. 
Si c > 0 la imagen se aclara (mas brillante), si c < 0 la imagen se oscurece.
- Con "a" se cambia el contraste de la imagen.
Si a > 1 amplificacion, si 0 < a < 1 disminucion (abajo explico por que no a=0).
- Si s = -r (seria a = -1 y c = 0) se obtiene el negativo de la imagen.

Otras cosas para tener en cuenta:

-El valor de "a" no puede ser 0, porque si es 0 la imagen se vuelve negra o de un color "c" 
constante, ya que s = 0*r + c = c.

-Para obtener el negativo de la imagen se utiliza a = -1, pero se hace una renormalizacion para
tener los valores positivos, ya que no podemos tener valores negativos en la imagen. 
Para eso, como vimos en la teoria, se hace s = -r + rmax, donde ese rmax es el valor maximo 
de la imagen original. Entonces, si la imagen original es de 8 bits, rmax = 255 (que es el 
valor maximo de "c").

-Los parámetros "a" y "c" en una transformación lineal representan la pendiente y la intersección 
con el eje y, respectivamente, en la ecuación de una línea recta y = ax + c
"""

PATH = "../images/"

WINDOWS_1 = "Controles"
WINDOWS_2 = "Imagen transformada"

# Inicializo una ventana para los controles y creo otra ventana para mostrar la imagen transformada
cvui.init(WINDOWS_1)
cv2.namedWindow(WINDOWS_2)

# Leer la imagen en escala de grises
image = cv2.imread(PATH + "cameraman.tif", cv2.IMREAD_GRAYSCALE)

# Crear un vector (LUT) de 0 a 255
LUT = np.arange(256)

#* Funcion para aplicar la transformacion lineal a la imagen original
# No se modifica la LUT original porque sino se van acumulando cambios cada vez que se llama a la
# funcion y se desbordan los valores de la LUT
def apply_LUT(img, LUT, a, c):
    new_LUT = a*LUT[:] + c       # Aplicar la transformacion lineal
    new_LUT = np.clip(new_LUT, 0, 255)  # Clipping para que los valores no se salgan de 0 a 255
    return new_LUT[img]             # Aplicar la LUT a la imagen original

#* Interfaz grafica para controles
frame = np.zeros((280, 350, 3), np.uint8)

# Trackbars variables
pos_x = 10
width = 320
a = [1]
c = [0]
a_min, a_max = 1, 5
c_min, c_max = -255, 255    # para imagenes de 8 bits

# Checkbox variable
negative = [False]  # Checkbox para obtener el negativo de la imagen

#* Bucle principal
while True:
    frame[:] = (49, 52, 49)     # Fondo gris oscuro para la ventana de controles

    cvui.text(frame, pos_x, 20, 'Factor de ganancia')
    cvui.trackbar(frame, pos_x, 40, width, a, a_min, a_max)
    cvui.text(frame, pos_x, 110, 'Offset')
    cvui.trackbar(frame, pos_x, 130, width, c, c_min, c_max)

    # Checkbox para obtener el negativo de la imagen
    cvui.checkbox(frame, pos_x, 200, 'Activar negativo', negative)

    # Boton para resetear los valores de los trackbars
    if cvui.button(frame, pos_x, 230, width, 30, 'Resetear'):
        a[0] = 1
        c[0] = 0

    cvui.update()   # Actualizar la interfaz grafica
    cv2.imshow(WINDOWS_1, frame)    # Mostrar la ventana de controles

    # Aplicar la transformacion a la imagen de entrada
    if negative[0]:  # Si el checkbox está marcado, se obtiene el negativo (a=-1, c=rmax) de la imagen de entrada
        image_transformed = apply_LUT(image, LUT, -1, 255)
    else:  # Si no, se aplica la transformación lineal normal con los valores de los trackbars
        image_transformed = apply_LUT(image, LUT, a[0], c[0])

    # Convertir imagen transformada a enteros de 8 bits para poder mostrarla
    image_transformed = image_transformed.astype(np.uint8)

    #! FALTA CORREGIR ESTO PARA MOSTRAR EL MAPEO APLICADO (la parte del else)
    # Crear una imagen del mapeo aplicado
    mapping_image = np.zeros((256, 256), dtype=np.uint8)
    if negative[0]:
        cv2.line(mapping_image, (0, 0), (255, 255), 255, 1)
    else:
        end_y = min(int(a[0]*255+c[0]), 255)
        cv2.line(mapping_image, (0, 255), (255, 255-end_y), 255, 1)
    #! --------------------------------------------------
        
    # Apilar horizontalmente la imagen original, la imagen del mapeo y la imagen transformada
    combined_image = np.hstack((image, mapping_image, image_transformed))

    # Mostrar la imagen combinada
    cv2.imshow(WINDOWS_2, combined_image)

    if cv2.waitKey(20) == 27:   # Salir con ESC
        break