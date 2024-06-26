import cv2

def invert_colors(img):
    """
    Funcion para obtener una imagen con los colores complementarios.
    En color, el complementario se obtiene como el opuesto en el circulo cromatico
    mas el negativo de la intensidad.
    """
    # Convertir la imagen a HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Me quedo con el canal H (indice 0) ya que es el que contiene la informacion del color (Hue)
    h = img_hsv[:,:,0]

    # Invertir los colores
    # En el word con anotaciones deje bien explicado este doble for.
    # Recordar que en OpenCV los valores de H varian de 0 y 180, no de 0 a 360 como el circulo.
    # Eso es asi porque con 8 bits no podemos representar un numero mayor a 255.
    for x in range(h.shape[0]):
        for y in range(h.shape[1]):
            pixel = h[x,y]+90
            if pixel > 179:
                pixel = pixel-179
            h[x,y] = pixel
    
    # Actualizar el canal H de la imagen con los colores invertidos
    img_hsv[:,:,0] = h
    # Aplicar el negativo a la intensidad
    img_hsv[:,:,2] = 255 - img_hsv[:,:,2]
    
    return cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)