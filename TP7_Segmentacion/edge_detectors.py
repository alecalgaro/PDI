import cv2
import numpy as np

def prewitt(img):
    """
    Funcion que implementa el detector de bordes de Prewitt.
    k_x detecta bordes verticales (cambios de intensidad de izquierda a derecha)
    k_y detecta bordes horizontales (cambios de intensidad de arriba a abajo)
    k_d1 detecta bordes diagonales desde arriba a la izquierda hacia abajo a la derecha
    k_d2 detecta bordes diagonales desde abajo a la izquierda hacia arriba a la derecha
    """
    k_x = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    k_y = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    k_d1 = np.array([[-1,-1,0],[-1,0,1],[0,1,1]])  
    k_d2 = np.array([[0,1,1],[-1,0,1],[-1,-1,0]])  
    
    img_x = cv2.filter2D(img, cv2.CV_64F, k_x)
    img_y = cv2.filter2D(img, cv2.CV_64F, k_y)
    img_d1 = cv2.filter2D(img, cv2.CV_64F, k_d1)
    img_d2 = cv2.filter2D(img, cv2.CV_64F, k_d2)
    
    # Si solo se suman los bordes detectados por los 4 filtros, se obtiene una imagen
    # con los bordes detectados pero con un fondo de gris medio y bordes de distinta intensidad.
    # img = img_x + img_y + img_d1 + img_d2
    
    # Para obtener una imagen binaria con los bordes detectados, se puede sumar los bordes detectados
    # por los 4 filtros y luego aplicar un umbral para obtener una imagen binaria.
    img = np.sqrt(img_x**2 + img_y**2 + img_d1**2 + img_d2**2)
    img = (img > 0.1*np.max(img))*255

    return img

def sobel(img,dtype,ksize):
    """
    Funcion que implementa el detector de bordes de Sobel.
    """
    # Bordes detectados en direccion x
    img_sb_x = cv2.Sobel(img,dtype,1,0,ksize)
    # Bordes detectados en direccion y
    img_sb_y = cv2.Sobel(img,dtype,0,1,ksize)

    # Se suman los bordes detectados por los filtros de Sobel en x e y
    img_sb = img_sb_x + img_sb_y 
    
    # Si ksize es diferente de -1, se suman los bordes detectados por el filtro de Sobel en x e y
    # simultaneamente, para obtener bordes diagonales.
    # El ksize != -1 se utiliza porque el operador de Sobel con ksize=-1 es equivalente a usar un 
    # kernel de tamaño 3x3. Para un kernel de tamaño 3x3, la convolución en las direcciones x e y 
    # por separado es suficiente y no necesitamos hacer una convolución adicional en ambas 
    # direcciones simultáneamente.
    if ksize != -1:
        img_sb += cv2.Sobel(img,dtype,1,1,ksize,scale=2)
                            
    return img_sb

def laplacian(img,dtype,ksize):
    """
    Funcion que implementa el detector de bordes de Laplacian.
    """
    img_f = cv2.Laplacian(img, dtype, ksize)
    
    return img_f

def canny(img,minVal,maxVal,L2):
    """
    Funcion que implementa el detector de bordes de Canny.
    - img es la imagen de entrada. Debe ser una imagen en escala de grises.
    - minVal y maxVal son los umbrales para la histeresis. Los valores de intensidad
    de los bordes que son mayores a maxVal son considerados bordes y los
    valores de intensidad de los bordes que son menores a minVal se descartan. 
    Los valores de intensidad de los bordes que están entre minVal y maxVal son 
    considerados bordes dependiendo de si están conectados a bordes superiores 
    de maxVal o no.
    - L2gradient es un booleano que indica si se quiere usar L2 gradient.
    Si L2gradient es verdadero, encuentra la magnitud del gradiente usando la ecuación 
    sqrt{(dI/dx)^2 + (dI/dy)^2} (L2 norm), que es más exacta. Si es falso, utiliza la 
    ecuación |dI/dx| + |dI/dy| (L1 norm). Es opcional y su valor predeterminado es False.
    """
    return cv2.Canny(img, minVal, maxVal, L2gradient=L2)