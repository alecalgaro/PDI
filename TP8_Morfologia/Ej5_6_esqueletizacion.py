import cv2
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def esqueletizacion_morfologica(img):
    
    # Convertir a escala de grises
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Umbralizar la imagen para obtener una imagen binaria
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # Obtener el elemento estructurante para la morfología (puedes ajustar el tamaño según sea necesario)
    elemento_estructurante = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    
    # Inicializar la imagen esqueleto
    esqueleto = np.zeros(img_bin.shape, np.uint8)
    
    # Repetir la erosión y encontrar la imagen diferencia hasta que ya no haya cambios
    while True:
        # Erosión
        erodida = cv2.erode(img_bin, elemento_estructurante)
        # Apertura (erosión seguida de dilatación)
        temp = cv2.dilate(erodida, elemento_estructurante)
        # Diferencia entre la imagen binaria y su apertura
        temp = cv2.subtract(img_bin, temp)
        # OR lógico para actualizar el esqueleto
        esqueleto = cv2.bitwise_or(esqueleto, temp)
        img_bin = erodida.copy()
        
        # Si ya no hay cambios, romper el bucle
        if cv2.countNonZero(img_bin) == 0:
            break
    
    return esqueleto

# Cargar imagen
PATH = '../images/'
img = cv2.imread(PATH + 'cuerpos.jpg')
cv2.imshow('Imagen original', img)

# Aplicar algoritmo de esqueletizacion
esqueleto = esqueletizacion_morfologica(img)

# Mostrar el esqueleto
cv2.imshow('Esqueleto', esqueleto)
cv2.waitKey(0)
cv2.destroyAllWindows()