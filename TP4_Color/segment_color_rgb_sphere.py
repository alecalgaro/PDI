import cv2
import numpy as np
import cvui
import color_slicing as cs

def segment_color_rgb_sphere(image):
    """
    Funcion para aplicar el rebanado de color en RGB con el metodo de la esfera.
    Se recibe una imagen y se define el color central "a" y el radio R0 de la esfera de color.
    """
    # Crear una ventana para la imagen y otra para los controles
    WINDOW_NAME = 'Imagen segmentada'
    WINDOW_NAME_CONTROLS = 'Controles'
    cvui.init(WINDOW_NAME)
    cvui.init(WINDOW_NAME_CONTROLS)

    # Inicializar los valores de R, G, B y R0
    R = [0]
    G = [0]
    B = [0]
    R0 = [50]

    # Inicializar el estado del checkbox
    checkbox_state = [False]

    # Crear un frame para contener los trackbars y el checkbox
    UI = np.zeros((450, 300, 3), np.uint8)

    while True:
        # Llenar el frame con negro
        UI[:] = (49, 52, 49)

        # Crear los trackbars para R, G, B y R0
        cvui.text(UI, 50, 20, 'R')
        cvui.trackbar(UI, 50, 50, 150, R, 0, 255)
        cvui.text(UI, 50, 100, 'G')
        cvui.trackbar(UI, 50, 120, 150, G, 0, 255)
        cvui.text(UI, 50, 170, 'B')
        cvui.trackbar(UI, 50, 190, 150, B, 0, 255)
        cvui.text(UI, 50, 260, 'R0')
        cvui.trackbar(UI, 50, 280, 150, R0, 0, 255)

        # Crear el checkbox para mostrar la imagen segmentada o la máscara
        cvui.checkbox(UI, 50, 320, 'Mostrar mascara', checkbox_state)

        # Aplicar el rebanado de color en RGB
        # Definir el color central "a" y el radio R0 de la esfera de color
        a = np.array([R[0], G[0], B[0]])    # ajustar color de piel
        img_sliced_rgb, mask = cs.color_slicing_rgb_sphere(image, a, R0[0])

        # Mostrar la imagen segmentada o la máscara, dependiendo del estado del checkbox
        if checkbox_state[0]:
            cv2.imshow(WINDOW_NAME, mask)
        else:
            cv2.imshow(WINDOW_NAME, img_sliced_rgb)

        # Mostrar los controles
        cvui.imshow(WINDOW_NAME_CONTROLS, UI)

        # Salir del bucle si se presiona la tecla ESC
        if cv2.waitKey(20) == 27:
            break

    # Cerrar todas las ventanas
    cv2.destroyAllWindows()

    # Retornar la imagen segmentada y la máscara
    return img_sliced_rgb, mask