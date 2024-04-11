import cv2
import numpy as np
import cvui
import utils as ut
import os

DEFAULT_POS = [[50,50], [50,100], [50,150], [50,200], [50,250], [100,50],
               [100,100], [100,150], [100,200], [100,250]]

def detect_missing_pills(image, bg_th=100, positions=DEFAULT_POS):
    """TODO: Docstring for detect_missing_pills.

    Parameters:
        image: TODO
        bg_th: Umbral para el fondo. Todo lo que sea menor a este numero se
        considera fondo. Valor por defecto=100.
    Returns:
        TODO

    """
    mask = image < bg_th
    image=cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    missing_pills = []
    for pos in positions:
        if mask[pos[0], pos[1]] != 0:
            missing_pills.append(pos)
            cv2.rectangle(image, (pos[1]-15, pos[0]-15),
                          (pos[1]+15, pos[0]+15), (0, 0, 255), 1)
    return image


def load_image(NIMG, IMAGE_DIR):
    """Cargamos imagen dado el numero de la misma.

    Parameters:
        NIMG: ID de la imagen.
        IMAGE_DIR: Directorio con imagenes guardadas.
    Returns:
        imagen: Imagen cargada y procesada.

    """
    filename = f"{IMAGE_DIR}blister_{NIMG:02d}.jpg"
    imagen = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    imagen = detect_missing_pills(imagen)
    return imagen, filename


WINDOW_NAME = "Missing pills"
cvui.init(WINDOW_NAME)

NIMG = 1
IMAGE_DIR = "blisters/"
imagen, filename = load_image(NIMG, IMAGE_DIR)
width = imagen.shape[1]+40
height = imagen.shape[0]+60
max_nimg = len([f for f in os.listdir(IMAGE_DIR) if "blister_" in f])
frame = np.zeros((height, width, 3), np.uint8)

while True:
    frame[:] = (49, 52, 49)
    cvui.beginRow(frame, 10, 10, -1, -1, 20)
    if (cvui.button("Prev")):
        # The button was clicked, so let's decrement our counter.
        NIMG -= 1
        if NIMG < 1:
            NIMG = 1
        else:
            imagen, filename = load_image(NIMG, IMAGE_DIR)
    cvui.text(filename)
    if (cvui.button("Next")):
        # The button was clicked, so let's increment our counter.
        NIMG += 1
        if NIMG > max_nimg:
            NIMG = max_nimg
        else:
            imagen, filename = load_image(NIMG, IMAGE_DIR)
    cvui.endRow()

    cvui.beginRow(frame, 20, 50, -1, -1)
    cvui.image(imagen)
    cvui.endRow()

    # Update cvui internal stuff
    cvui.update()

    # Show window content
    cvui.imshow(WINDOW_NAME, frame)

    # Press ESC to exit
    if cv2.waitKey(20) == 27:
        break
