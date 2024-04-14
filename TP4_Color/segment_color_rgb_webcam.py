import cv2
import numpy as np
import cvui
import color_slicing as cs

def segment_color_rgb_webcam():
    """
    Funcion para segmentar color en RGB utilizando la webcam.
    """
    # Abrir la webcam (0)
    video = cv2.VideoCapture(0)

    WINDOW_NAME = 'Video segmentado'
    WINDOW_NAME_CONTROLS = 'Controles'
    cvui.init(WINDOW_NAME)
    cvui.init(WINDOW_NAME_CONTROLS)

    UI = np.zeros((580, 350, 3), np.uint8)

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

        # Crear los trackbars para los valores mínimos y máximos de cada canal de color en RGB
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

        # Crear los arrays lower y upper
        lower = np.array([b_min[0], g_min[0], r_min[0]])
        upper = np.array([b_max[0], g_max[0], r_max[0]])

        # Leer el siguiente fotograma del video
        ret, frame = video.read()

        # Si el fotograma no se leyó correctamente, salir del bucle
        if not ret:
            break

        # Aplicar el rebanado de color (el fotograma se convierte a RGB en la funcion)
        frame_slicing, mask = cs.color_slicing_rgb(frame, lower, upper)

        # Mostrar la mascara o la segmentacion dependiendo del estado del checkbox
        if show_mask[0]:
            cvui.imshow(WINDOW_NAME, mask)
        else:
            cvui.imshow(WINDOW_NAME, frame_slicing)

        # Mostrar los controles
        cvui.imshow(WINDOW_NAME_CONTROLS, UI)

        # Salir del bucle si se presiona la tecla ESC
        if cv2.waitKey(20) == 27:
            break

    video.release()
    cv2.destroyAllWindows()