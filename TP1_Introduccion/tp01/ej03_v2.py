import cv2
import numpy as np
import cvui
import os


def detect_bottles(image, bg_th=10):
    """Contamos cuantas veces cambia de botella a fondo aprovechando que el
    fondo tiende a ser negro. Tomamos como fondo todo lo que tenga intensidad
    menor a bg_th. Se obtiene como salida una lista de tuplas donde cada tupla
    indica los limites en x de cada botella.

    Parameters:
        image: Imagen a analizar.
        bg_th: Umbral para el fondo. Todo lo que sea menor a este numero se
        considera fondo. Valor por defecto=10.
    Returns:
        xlims: Lista de la forma [(xmin1, xmax1), (xmin2, xmax2), ...] donde
        cada tupla corresponde a los limites de una botella.

    """

    # Tomamos una fila a la mitad de la imagen (algo donde sea evidente desde
    # donde y hasta donde van las botellas). El ultimo parece que siempre es
    # blanco asi que no lo contamos (total no vamos a tener una botella de 2
    # pixeles de ancho).
    row = image[image.shape[0]//2,:-1]

    # Para determinar si empezamos a contar fondo o botella, nos basamos en el
    # primer pixel.
    is_bottle = row[0] > bg_th
    xlims=[]
    xmin, xmax = 0, 0

    # Recorremos la fila registrando los cambios en las intensidades. Para
    # registrar bien el ultimo pixel, lo hacemos luego
    for x in range(1, len(row)-1):
        if is_bottle and row[x] < bg_th:
            is_bottle = False
            xmax=x
            xlims.append((xmin, xmax))

        if not is_bottle and row[x] > bg_th:
            is_bottle = True
            xmin = x-1

    # Terminamos con el ultimo pixel
    if is_bottle:
        xmax=len(row)-1
        xlims.append((xmin, xmax))

    return xlims


def detect_filled_level(image, xlims, lq_th=200):
    """Detectamos el nivel de llenado de las botellas. Para eso tomamos los
    centros de cada botella (tomando como referencia los limites de xlims) y
    recorremos hasta obtener el nivel de llenado que coincide con el cambio de
    botella a liquido. Se considera liquido lo que esta por encima de bg_th y
    por debajo de lq_th.

    Parameters:
        image: Imagen a analizar.
        xlims: Lista de la forma [(xmin1, xmax1), (xmin2, xmax2), ...] donde
        cada tupla corresponde a los limites de una botella.
        lq_th: Umbral para el liquido. Todo lo que sea mayor a este numero se
        considera botella y lo menor, fondo.
    Returns:
        ylims: Lista de numeros donde cada uno indica la altura a la que se
        encuentra el liquido de cada botella.
        ymin: El valor mas bajo en Y que puede tomar un nivel. Numericamente
        es el mas alto porque el eje Y crece hacia abajo.

    """

    # Como la camara esta fija, siempre deberia arrancar por el fondo. Luego
    # deberia empezar el pico de la botella y de ahi al final. Los dos ultimos
    # pixeles corresponden a la cinta transportadora asi que se ignoran.
    ylims = []
    for lim in xlims:
        x = lim[0]+(lim[1]-lim[0])//2
        column = image[:-2, x]
        is_bottle = False
        ylev = len(column)
        for y in range(len(column)):
            if is_bottle and column[y] < lq_th:
                is_bottle = False
                ylev = y
            if not is_bottle and column[y] > lq_th:
                is_bottle = True
        ylims.append(ylev)

    return ylims, len(column)


def compute_percentages(ylims, ymin):
    """Calculamos los porcentajes de llenado a partir de comparar el punto mas
    alto. Asumimos que al menos una botella esta llena...

    Parameters:
        ylims: Lista de numeros donde cada uno indica la altura a la que se
        encuentra el liquido de cada botella.
        ymin: El valor mas bajo en Y que puede tomar un nivel. Numericamente
        es el mas alto porque el eje Y crece hacia abajo.
    Returns:
        percs: Lista de porcentajes de llenado de cada botella.
        ymax: El valor mas alto en Y que puede tomar un nivel. Numericamente
        es el mas bajo porque el eje Y crece hacia abajo. Asumimos que hay al
        menos una botella llena y se toma como referencia para medir.

    """
    ymax = min(ylims)
    percs = [100*(ymin-y)/(ymin-ymax) for y in ylims]
    return percs, ymax


def draw_predictions(image, xlims, ylims, ymin, ymax, percs):
    """Dibujamos rectangulos y lineas para indicar la posicion y el porcentaje
    de llenado.

    Parameters:
        image: Imagen a editar.
        xlims: Lista de la forma [(xmin1, xmax1), (xmin2, xmax2), ...] donde
        cada tupla corresponde a los limites de una botella.
        ylims: Lista de numeros donde cada uno indica la altura a la que se
        encuentra el liquido de cada botella.
        ymin: El valor mas bajo en Y que puede tomar un nivel. Numericamente
        es el mas alto porque el eje Y crece hacia abajo.
        ymax: El valor mas alto en Y que puede tomar un nivel. Numericamente
        es el mas bajo porque el eje Y crece hacia abajo. Asumimos que hay al
        percs: Lista de porcentajes de llenado de cada botella.
    Returns:
        new_image: Imagen modificada para ser dibujada externamente.

    """
    image=cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for i in range(len(xlims)):
        COLOR = (0, 0, 255) if percs[i]<100 else (0, 255, 0)
        cv2.rectangle(image, (xlims[i][0], ymin), (xlims[i][1], ymax),
                      COLOR)
        cv2.line(image, (xlims[i][0], ylims[i]), (xlims[i][1], ylims[i]),
                 COLOR, 2, cv2.LINE_8)
        cv2.putText(image, f"{percs[i]:.2f}%", (xlims[i][0]+1,ylims[i]-5), 0,
                    0.4, COLOR, 1)
    return image


def load_image(NIMG, IMAGE_DIR):
    """Cargamos imagen dado el numero de la misma.

    Parameters:
        NIMG: ID de la imagen.
        IMAGE_DIR: Directorio con imagenes guardadas.
    Returns:
        imagen: Imagen cargada y procesada.

    """
    filename = f"{IMAGE_DIR}botellas_{NIMG:02d}.tif"
    imagen = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    xlims = detect_bottles(imagen)
    ylims, min_y = detect_filled_level(imagen, xlims)
    percs, max_y = compute_percentages(ylims, min_y)
    imagen = draw_predictions(imagen, xlims, ylims, min_y, max_y, percs)
    return imagen, filename

WINDOW_NAME = "Filled bottles"

cvui.init(WINDOW_NAME)

NIMG = 1
IMAGE_DIR = "botellas/"
imagen, filename = load_image(NIMG, IMAGE_DIR)
width = imagen.shape[1]+40
height = imagen.shape[0]+60
max_nimg = len([f for f in os.listdir(IMAGE_DIR) if "botellas_" in f])
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


