import cv2
import numpy as np
import cvui
import color_slicing as cs

def segment_color_hsv_image(image):
    """
    Funcion para segmentar color en una imagen en el modelo de color HSV.
    Recibe una imagen y devuelve la imagen segmentada y la mascara.
    """

    # Crear una ventana para la imagen y otra para los controles
    WINDOW_NAME = 'Imagen segmentada'
    WINDOW_NAME_CONTROLS = 'Controles'
    cvui.init(WINDOW_NAME)
    cvui.init(WINDOW_NAME_CONTROLS)

    UI = np.zeros((580, 350, 3), np.uint8)

    # Valores iniciales para los trackbars
    h_min = [0]
    s_min = [0]
    v_min = [0]
    h_max = [179]
    s_max = [255]
    v_max = [255]

    # Valor del checkbox para mostrar la mascara o la segmentacion
    show_mask = [False]

    while True:
        UI[:] = (49, 52, 49)

        # Crear los trackbars para los valores mínimos y máximos de cada canal de color en HSV
        cvui.text(UI, 10, 30, 'H min')
        cvui.trackbar(UI, 10, 50, 300, h_min, 0, 179)
        cvui.text(UI, 10, 120, 'H max')
        cvui.trackbar(UI, 10, 140, 300, h_max, 0, 179)
        cvui.text(UI, 10, 210, 'S min')
        cvui.trackbar(UI, 10, 230, 300, s_min, 0, 255)
        cvui.text(UI, 10, 300, 'S max')
        cvui.trackbar(UI, 10, 320, 300, s_max, 0, 255)
        cvui.text(UI, 10, 380, 'V min')
        cvui.trackbar(UI, 10, 400, 300, v_min, 0, 255)
        cvui.text(UI, 10, 470, 'V max')
        cvui.trackbar(UI, 10, 490, 300, v_max, 0, 255)

        # Crear el checkbox para mostrar la mascara o la segmentacion
        cvui.checkbox(UI, 10, 550, 'Mostrar mascara', show_mask)

        # Crear los arrays lower y upper
        lower = np.array([h_min[0], s_min[0], v_min[0]])
        upper = np.array([h_max[0], s_max[0], v_max[0]])

        # Aplicar el rebanado de color (la imagen se convierte a HSV en la funcion)
        img_slicing, mask = cs.color_slicing_hsv(image, lower, upper)

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

    return img_slicing, mask