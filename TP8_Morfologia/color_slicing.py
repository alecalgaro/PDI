import cv2
import numpy as np

def color_slicing_rgb_sphere(img, a, R0):
    """
    Funcion para rebanado de color (color slicing) en una imagen en el espacio de color RGB.
    Se recibe una imagen en BGR y un color central "a" en [B,G,R] y un radio R0 de la esfera
    para hacer el mapeo de colores en una esfera de radio R0 centrada en "a".
    
    (Formula implementada y mas informacion en pag. 31 del PDF de teoria de color).
    """
    # Convertir la imagen a float32 para evitar desbordamientos
    img = img.astype(np.float32)

    # Calcular la distancia desde cada pixel hasta el centro de color "a"
    # con (img - a) calcula la diferencia en cada canal de color (RGB) con el color del color 
    # central "a". Luego al elevar al cuadrado y sumar esas distancias se obtiene la distancia 
    # euclidiana, desde cada px al color central "a".
    # axis=2 es para que se sumen las distancias en cada canal de color (eje 0 y 1 son el ancho
    # y el alto de la imagen, y el eje 2 es el de los canales de color RGB)
    dist = np.sum((img - a)**2, axis=2)

    # Crear una mascara para los pixeles que estan dentro de la "rebanada" de color,
    # que seran aquellos cuya distancia es menor a un valor R0 definido.
    # En mask se guarda True en una posicion si la distancia es menor a R0 y False si es mayor. 
    # Como antes se calcula el cuadrado de la distancia, se compara con R0**2, porque es mas eficiente
    # calcular el cuadrado que la raiz cuadrada que deberia calcular en  dist = np.sqrt(np.sum((img - a)**2, axis=2))
    mask = dist < (R0**2)

    # Colocar un color fijo a los pixeles que están fuera de la "rebanada"
    img_sliced = img.copy()
    img_sliced[mask == False] = [0, 0, 0]  # en la formula de teoria usa 0.5 (128) pero le puse negro
    # Para recordar: otra forma de invertir la mascara es con el operador ~ en Python, haciendo:
    # img_sliced[~mask] = [128, 128, 128]

    # Convertir la imagen de vuelta a uint8
    img_sliced = img_sliced.astype(np.uint8)

    # Convertir la mascara a uint8 (para que no sea booleana y poder mostrarla)
    mask = (mask * 255).astype(np.uint8)

    return img_sliced, mask

def color_slicing_rgb(img, lower, upper):
    """
    Funcion para rebanado de color (color slicing) en una imagen en el espacio de color RGB.
    Recibe la imagen y dos arrays con los valores minimo y maximo de cada canal.
    Devuelve una imagen en el mismo espacio de color que la imagen de entrada.
    """
    # Convertir lower y upper a arrays de numpy del mismo tipo de datos que la imagen de entrada
    lower = np.array(lower, dtype=img.dtype)
    upper = np.array(upper, dtype=img.dtype)
    
    # Crear una mascara para los pixeles que están dentro del rango de color
    mask = cv2.inRange(img, lower, upper)

    # Aplicar la mascara a la imagen
    img_sliced = cv2.bitwise_and(img, img, mask=mask)

    return img_sliced, mask

def color_slicing_hsv(img, lower, upper):
    """
    Funcion para rebanado de color (color slicing) en una imagen en el espacio de color HSV.
    Devuelve una imagen en el mismo espacio de color que la imagen de entrada.
    """
    # Convertir la imagen a HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Convertir lower y upper a arrays de numpy del mismo tipo de datos que la imagen
    lower = np.array(lower, dtype=img_hsv.dtype)
    upper = np.array(upper, dtype=img_hsv.dtype)

    # Crear una mascara para los pixeles que estan dentro del rango de color
    mask = cv2.inRange(img_hsv, lower, upper)

    # Aplicar la mascara a la imagen
    img_sliced = cv2.bitwise_and(img, img, mask=mask)

    return img_sliced, mask