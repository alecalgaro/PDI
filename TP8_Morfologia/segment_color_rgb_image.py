import cv2
import numpy as np
import cvui
import color_slicing as cs

def segment_color_rgb_image(image):
    """
    Funcion para segmentar color en una imagen en el modelo de color RGB.
    Recibe una imagen y devuelve la imagen segmentada y la mascara.
    """

    # Crear una ventana para la imagen y otra para los controles
    WINDOW_NAME = 'Imagen segmentada'
    WINDOW_NAME_CONTROLS = 'Controles'
    cvui.init(WINDOW_NAME)
    cvui.init(WINDOW_NAME_CONTROLS)

    # Crear una imagen en blanco para los controles
    UI = np.zeros((620, 350, 3), np.uint8)

    # Valores iniciales para los trackbars
    r_min = [0]
    g_min = [0]
    b_min = [0]
    r_max = [255]
    g_max = [255]
    b_max = [255]

    # Valor del checkbox para mostrar la mascara o la segmentacion
    show_mask = [False]

    while True:
        UI[:] = (49, 52, 49)

        # Crear los trackbars para los valores minimos y maximos de cada canal de color
        cvui.text(UI, 10, 30, 'R min')
        cvui.trackbar(UI, 10, 50, 300, r_min, 0, 255)
        cvui.text(UI, 10, 120, 'R max')
        cvui.trackbar(UI, 10, 140, 300, r_max, 0, 255)
        cvui.text(UI, 10, 210, 'G min')
        cvui.trackbar(UI, 10, 230, 300, g_min, 0, 255)
        cvui.text(UI, 10, 300, 'G max')
        cvui.trackbar(UI, 10, 320, 300, g_max, 0, 255)
        cvui.text(UI, 10, 380, 'B min')
        cvui.trackbar(UI, 10, 400, 300, b_min, 0, 255)
        cvui.text(UI, 10, 470, 'B max')
        cvui.trackbar(UI, 10, 490, 300, b_max, 0, 255)

        # Crear el checkbox para mostrar la mascara o la segmentacion
        cvui.checkbox(UI, 10, 550, 'Mostrar mascara', show_mask)

        # Crear el boton para salir del bucle
        if cvui.button(UI, 10, 580, 'Aceptar'):
            break

        # Crear los arrays lower y upper
        lower = np.array([b_min[0], g_min[0], r_min[0]])
        upper = np.array([b_max[0], g_max[0], r_max[0]])

        # Aplicar el rebanado de color
        img_slicing, mask = cs.color_slicing_rgb(image, lower, upper)

        # Mostrar la mascara o la segmentacion dependiendo del estado del checkbox
        if show_mask[0]:
            cvui.imshow(WINDOW_NAME, mask)
        else:
            cvui.imshow(WINDOW_NAME, img_slicing)

        # Mostrar los controles
        cvui.imshow(WINDOW_NAME_CONTROLS, UI)

        # Salir del bucle si se presiona la tecla ESC
        if cv2.waitKey(20) == 27:
            break

    cv2.destroyAllWindows()

    # Al salir del bucle se devuelve la imagen segmentada y la mascara
    return img_slicing, mask