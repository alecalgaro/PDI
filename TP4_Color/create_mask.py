import cv2
import numpy as np

def create_mask(image, input_points=None):
    """
    Funcion para crear una mascara a partir de seleccionar puntos en una imagen con el click del
    mouse o utilizando un arreglo de vertices.
    Se recibe la imagen y opcionalmente un arreglo de vertices para utilizar, y se devuelve la 
    imagen con la mascara aplicada y la mascara binaria.

    El poligono se crea usando los puntos seleccionados o recibidos como parametros, por lo cual, 
    si se desea crear un cuadrado o rectangulo, los puntos se deben seleccionar en orden horario 
    o antihorario. Si se seleccionan con el mouse, para finalizar se presiona la tecla "c".
    """

    # Lista para almacenar los puntos
    points = []

    # Funcion callback del evento del mouse
    def select_points(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Guardar las coordenadas del punto seleccionado
            points.append((x, y))

    # Crear una ventana y asignar la funcion callback del mouse
    WINDOWS_NAME = "Crear mascara"
    cv2.namedWindow(WINDOWS_NAME)
    cv2.setMouseCallback(WINDOWS_NAME, select_points)

    # Se no se reciben puntos, se seleccionan con el mouse
    if input_points is None:
        while True:
            # Mostrar la imagen
            cv2.imshow(WINDOWS_NAME, image)

            # Salir si se presiona la tecla "c"
            if cv2.waitKey(1) & 0xFF == ord("c"):
                break
    else:   # Si se reciben puntos por parametro, se utilizan
        points = input_points

    # Cerrar todas las ventanas
    cv2.destroyAllWindows()

    # Crear una imagen negra del mismo tamaño que la imagen original
    mask = np.zeros_like(image)

    # Crear mascara binaria dibujando un poligono blanco en la imagen negra, 
    # usando los puntos seleccionados
    cv2.fillPoly(mask, np.array([points], dtype=np.int32), (255,255,255))

    # Aplicar la mascara a la imagen
    image_with_mask = cv2.bitwise_and(image, mask)

    return image_with_mask, mask