import cv2
import numpy as np
import cvui

def create_mask(image, input_points=None):
    """
    Funcion para crear una mascara a partir de seleccionar puntos en una imagen con el click del
    mouse o utilizando un arreglo de vertices.
    Se recibe la imagen y opcionalmente un arreglo de vertices para utilizar, y se devuelve la 
    imagen con la mascara aplicada y la mascara binaria.

    El poligono se crea usando los puntos seleccionados o recibidos como parametros, por lo cual, 
    si se desea crear un cuadrado o rectangulo, los puntos se deben seleccionar en orden horario 
    o antihorario. Ademas se muestra una ventana con instrucciones para el usuario.
    """

    # Lista para almacenar los puntos
    points = []

    # Crear una copia de la imagen para dibujar los puntos y las lineas
    image_copy = image.copy()

    # Funcion callback del evento del mouse
    def select_points(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Guardar las coordenadas del punto seleccionado
            points.append((x, y))

            # Dibujar un circulo en el punto seleccionado
            cv2.circle(image_copy, (x, y), 5, (0, 255, 0), -1)

            # Dibujar una linea desde el ultimo punto al nuevo punto
            if len(points) > 1:
                cv2.line(image_copy, points[-2], points[-1], (0, 255, 0), 2)

    # Crear una ventana y asignar la funcion callback del mouse
    WINDOWS_NAME = "Crear mascara"
    cv2.namedWindow(WINDOWS_NAME)
    cv2.setMouseCallback(WINDOWS_NAME, select_points)

    # Crear una ventana para las instrucciones
    INSTRUCTIONS_WINDOW = "Instrucciones"
    cv2.namedWindow(INSTRUCTIONS_WINDOW)
    instructions_frame = np.zeros((180, 420, 3), np.uint8)
    cvui.init(INSTRUCTIONS_WINDOW)

    # Se no se reciben puntos, se seleccionan con el mouse
    if input_points is None:
        while True:
            # Mostrar la imagen
            cv2.imshow(WINDOWS_NAME, image_copy)

            # Mostrar las instrucciones
            instructions_frame[:] = (50, 50, 50)
            cvui.text(instructions_frame, 10, 10, "Seleccione los puntos con el mouse para crear la mascara.")
            cvui.text(instructions_frame, 10, 30, "Se creara un poligono, por lo tanto, los puntos deben ser")
            cvui.text(instructions_frame, 10, 50, "seleccionados en orden y se conectara automaticamente el")
            cvui.text(instructions_frame, 10, 70, "primer y ultimo punto elegido.")
            cvui.text(instructions_frame, 10, 110, "Presione el boton 'Aceptar' o la tecla 'ESC' para finalizar.")

            if cvui.button(instructions_frame, 10, 130, "Aceptar"):
                break
            
            # Mostrar ventana con instrucciones
            cvui.imshow(INSTRUCTIONS_WINDOW, instructions_frame)

            # Salir del bucle si se presiona la tecla ESC
            if cv2.waitKey(20) == 27:
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

    # Aplicar la mascara a la imagen original
    image_with_mask = cv2.bitwise_and(image, mask)

    # Retornar la imagen con la mascara aplicada y la mascara binaria
    return image_with_mask, mask