import numpy as np

# Filtro pasa-bajos ideal en frecuencia.
# Matriz de ceros, del mismo tamaño que la imagen.
# Desde el centro, se crea un circulo de radio D0 (frecuencia de corte), y dentro de ese 
# circulo se pone todo 1.

# Al recibir la dft, se toman solo las dos primeras dimensiones [:2] porque la dft tiene
# una dimension mas para la parte real y la imaginaria pero no nos interesa al aplicar el filtro.

# La version 2 es aplicando la formula que vimos en teoria, por eso hice el doble for,
# que si se usa con un solo valor de D0 no hay problema, pero si se utiliza un trackbar para
# ir variando el valor de D0 consume mucho, entonces hice otra version mas simple y eficiente.

#* Version mas eficiente sin doble for
def create_filter_PB_ideal(dft, D0):
    """
    Funcion que crea un filtro pasa-bajos ideal.
    Recibe la TDF y la frecuencia de corte D0 (radio del circulo).
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.zeros((rows, cols, 2), np.uint8)
    mask[crow-D0:crow+D0, ccol-D0:ccol+D0] = 1  # Circulo de radio D0 centrado en el centro y con todo 1
    return mask

#* Version con doble for
def create_filter_PB_ideal_v2(dft, D0):
    """
    Funcion que crea un filtro pasa-bajos ideal.
    Recibe la TDF y la frecuencia de corte D0 (radio del circulo).
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    mask = np.zeros_like(dft)   # Mascara de ceros del mismo tamaño que la TDF
    rows, cols = dft.shape[:2]  # Filas y columnas de la TDF
    center = (rows//2, cols//2)  # Centro de la TDF
    # Si la distancia desde el punto (u,v) al centro es menor a D0, se pone 1
    for u in range(rows):
        for v in range(cols):
            if np.sqrt((u-center[0])**2 + (v-center[1])**2) < D0:
                mask[u,v] = 1
    return mask