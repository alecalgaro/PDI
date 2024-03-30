import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui

"""
Implemente una funcion que realice las siguientes operaciones aritmeticas
sobre dos imagenes que sean pasadas como parametros:

a) Suma. Normalice el resultado por el numero de imagenes.
b(x,y) = (1-alpha)*f(x,y) + alpha*g(x,y)  con 0 <= alfa <= 1
"""

#* Dejo dos opciones de suma, una usando la funcion cv2.add o sumando simplemente, y otra usando
#* la funcion cv2.addWeighted que aplica la suma ponderada de dos arreglos. Ambas dan el mismo resultado
#* Ambas hacen el "alpha blending" o mezcla lineal que menciona en la teoria.

def suma(img1, img2, alpha):
    # Asegurarse de que las imágenes tienen el mismo tamaño
    assert img1.shape == img2.shape, "Las imágenes deben tener el mismo tamaño"

    # Convertir las imágenes a float32 para evitar desbordamiento, ya que si un px en  
    # unit8 supera 255, se vuelve a 0 y se pierde información. No es lo mismo que np.clip
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    sum_img = (1-alpha) * img1 + alpha * img2
    # sum_img = cv2.add(img1, img2) / 2     # Otra forma de hacer la suma
    sum_img = np.clip(sum_img, 0, 255)  # Limitar los valores al rango de 0 a 255

    # Convertir la imagen resultante de vuelta a uint8 para mostrarla
    sum_img = sum_img.astype(np.uint8)

    return sum_img

def alpha_blending(img1, img2, alpha):
    # Asegurarse de que las imágenes tienen el mismo tamaño
    assert img1.shape == img2.shape, "Las imágenes deben tener el mismo tamaño"

    # Convertir las imágenes a float32 para evitar desbordamiento, ya que si un px en  
    # unit8 supera 255, se vuelve a 0 y se pierde información. No es lo mismo que np.clip
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    # b(x,y) = (1-alpha)*f(x,y) + alpha*g(x,y) con 0 <= alfa <= 1
    blend_img = cv2.addWeighted(img1, (1 - alpha), img2, alpha, 0)
    blend_img = np.clip(blend_img, 0, 255)  # Limitar los valores al rango de 0 a 255

    # Convertir la imagen de vuelta a uint8 para poder mostrarla
    blend_img = blend_img.astype(np.uint8)

    return blend_img

#* La fusion de imagenes es simplemente un promedio de las imagenes (sin alpha), se suman todas y
#* se divide por la cantidad de imagenes. La hice porque se muestra en la teoria debajo de la suma

def fusion(img1, img2):
    # Asegurarse de que las imágenes tienen el mismo tamaño
    assert img1.shape == img2.shape, "Las imágenes deben tener el mismo tamaño"

    # Convertir las imágenes a float32 para evitar desbordamiento, ya que si un px en  
    # unit8 supera 255, se vuelve a 0 y se pierde información. No es lo mismo que np.clip
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    # Sumar las imágenes
    result = (img1 + img2)/2
    result = np.clip(result, 0, 255)  # Limitar los valores al rango de 0 a 255

    # Convertir la imagen de vuelta a uint8 para poder mostrarla
    result = result.astype(np.uint8)

    return result

#* Carga de imagenes y uso de las funciones

PATH = "../images/"

img1 = cv2.imread(PATH + "futbol.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(PATH + "chairs.jpg", cv2.IMREAD_GRAYSCALE)

# Redimensionar las imagenes para que tengan el mismo tamaño
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# Interfaz grafica
WINDOW_NAME = "Alpha Blending"
cvui.init(WINDOW_NAME)
frame = np.zeros((100, 700), np.uint8)
pos_x = 50
width = 600
alpha = [0.5]  # Valor actual de alpha para la mezcla
alpha_min, alpha_max = 0, 1
tam_paso = 0.1  # Tamaño del paso al mover el trackbar
# "%.2Lf" es el formato para mostrar el valor de alpha con dos decimales
# cvui.TRACKBAR_DISCRETE es para que el valor de alpha solo tenga valores discretos
# 0.1 es el paso de los valores discretos del trackbar

while True:
    # Crear un trackbar para controlar el valor de alpha
    cvui.trackbar(frame, pos_x, 30, width, alpha, alpha_min, alpha_max, tam_paso, "%.2Lf", cvui.TRACKBAR_DISCRETE, 0.1)

    # Aplicar las funciones
    result_sum = suma(img1, img2, alpha[0])
    result_blend = alpha_blending(img1, img2, alpha[0])
    result_fusion = fusion(img1, img2)

    # Mostrar las imagenes
    cv2.imshow("Suma", result_sum)
    cv2.imshow("Mezcla", result_blend)
    cv2.imshow("Fusion", result_fusion)

    # Actualizar la ventana de cvui
    cvui.imshow(WINDOW_NAME, frame)

    # Salir si se presiona la tecla ESC
    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()