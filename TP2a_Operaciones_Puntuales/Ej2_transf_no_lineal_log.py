import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui

"""
Transformaciones no lineales.
Implemente la transformacion logaritmica s = c*log(1+r) 
y la transformacion de potencia s = c*r^gamma 
(Utilizando c=1).

-Transformacion logaritmica:
Utilizada cuando la imagen de entrada tiene un rango dinámico grande, expande
las intensidades oscuras y comprime las intensidades claras.

-Transformacion exponencial:
Utilizada cuando la imagen de entrada tiene un rango dinámico bajo, expande
las intensidades claras y comprime las intensidades oscuras.
El valor de gamma se utiliza para controlar el brillo de una imagen.
gamma < 1 --> oscurece la imagen y se utiliza para aclarar imágenes que son muy brillantes.
gamma > 1 --> 1 aclara la imagen y se utiliza para oscurecer imágenes que son muy oscuras.
gamma = 1 --> no cambia la imagen.
"""

PATH = "../images/"

WINDOWS_1 = "Controles"
WINDOWS_2 = "Imagen transformada"

# Inicializo una ventana para los controles y creo otra ventana para mostrar la imagen transformada
cvui.init(WINDOWS_1)
cv2.namedWindow(WINDOWS_2)

# Leer la imagen en escala de grises
image = cv2.imread(PATH + "imagenE.tif", cv2.IMREAD_GRAYSCALE)

# Crear un vector (LUT) de 0 a 255
LUT = np.arange(256)   

#* Funcion para aplicar la transformacion logaritmica a la imagen original
#! CORREGIR ESTA FUNCION PORQUE AL COMENZAR LA IMAGEN SE VE NEGRA,
#! AL PONER C=5 APENAS SE VE LA IMAGEN
def apply_log_transformation(img, LUT, c):
    new_LUT = c * np.log(1 + LUT)    # s = c * log(1+r)
    new_LUT = np.clip(new_LUT, 0, 255)
    return new_LUT[img]

#* Funcion para aplicar la transformacion de potencia a la imagen original
def apply_power_transformation(img, LUT, gamma, c):
    new_LUT = c * np.power(LUT, gamma)   # s = c * r^gamma (c=1)
    new_LUT = np.clip(new_LUT, 0, 255)
    return new_LUT[img]

#* Interfaz grafica para controles
frame = np.zeros((280, 350, 3), np.uint8)

# Trackbars variables
pos_x = 10
width = 320
gamma = [1]
gamma_min, gamma_max = 0.1, 5
c = [1]    # c=1 como pide el enunciado pero creo un trackbar para modificarlo
c_min, c_max = 0.1, 5

# Checkbox variables
check_log = [True]
check_exp = [False]

#* Bucle principal
while True:
    frame[:] = (49, 52, 49)     # Fondo gris oscuro para la ventana de controles

    cvui.text(frame, pos_x, 20, 'Gamma')
    cvui.trackbar(frame, pos_x, 40, width, gamma, gamma_min, gamma_max)

    cvui.text(frame, pos_x, 100, 'c')
    cvui.trackbar(frame, pos_x, 120, width, c, c_min, c_max)

    cvui.checkbox(frame, pos_x, 200, 'Aplicar transformacion logaritmica', check_log)
    cvui.checkbox(frame, pos_x, 230, 'Aplicar transformacion exponencial', check_exp)

    cvui.update()   # Actualizar la interfaz grafica
    cv2.imshow(WINDOWS_1, frame)    # Mostrar la ventana de controles

    # Aplicar la transformacion log y exp a la imagen de entrada segun los checkbox
    if check_log[0]:
        image_transformed = apply_log_transformation(image, LUT, c[0])
    elif check_exp[0]:
        image_transformed = apply_power_transformation(image, LUT, gamma[0], c[0])

    # Convertir imagen transformada a enteros de 8 bits para poder mostrarla
    image_transformed = image_transformed.astype(np.uint8)

    cv2.imshow(WINDOWS_2, image_transformed)

    if cv2.waitKey(20) == 27:   
        break
