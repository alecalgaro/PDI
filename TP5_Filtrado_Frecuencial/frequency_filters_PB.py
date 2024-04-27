import numpy as np

#? ------------------------ FILTROS PASA-BAJOS EN FRECUENCIA ------------------------

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
def filter_PB_ideal(dft, D0):
    """
    Funcion que crea un filtro pasa-bajos ideal.
    Recibe la TDF y la frecuencia de corte D0 (radio del circulo).
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.zeros((rows, cols, 2), np.float32)
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - crow)**2 + (y - ccol)**2 <= D0**2
    mask[mask_area] = 1  # Circulo de radio D0 centrado en el centro y con todo 1
    return mask

#* Version del PB ideal con doble for
def filter_PB_ideal_v2(dft, D0):
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
            if np.sqrt((u-center[0])**2 + (v-center[1])**2) <= D0:
                mask[u,v] = 1
    return mask

def filter_PB_butterworth(dft_img, D0, n):
    """
    Filtro pasa-bajos Butterworth de orden "n".
    Recibe la TDF, la frecuencia de corte D0 y el orden del filtro.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    x = np.arange(-cols//2, cols//2)
    y = np.arange(-rows//2, rows//2)
    xx, yy = np.meshgrid(x, y)
    mask_2D = 1 / (1 + (np.sqrt(xx**2 + yy**2) / D0)**(2*n))    # Formula del filtro pasa-bajos Butterworth

    # Crear una mascara 3D con la misma forma que dft_img
    mask = np.zeros_like(dft_img)
    mask[:, :, 0] = mask_2D  # Llenar la primera capa de la mascara con mask_2D
    mask[:, :, 1] = mask_2D  # Llenar la segunda capa de la mascara con mask_2D
    return mask

#* Version con doble for pero sin raiz cuadrada
# Para evitar usar la raiz cuadrada, se modifica la formula del filtro Butterworth
# usando 1 / (1 + (D(u,v) / D0^2)^n)
def filter_PB_butterworth_v2(dft_img, D0, n):
    """
    Filtro pasa-bajos Butterworth de orden "n".
    Recibe la TDF, la frecuencia de corte D0 y el orden del filtro.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.zeros((rows, cols, 2), np.float32)

    for i in range(rows):
        for j in range(cols):
            dist = (i - crow)**2 + (j - ccol)**2  # Distancia al centro
            mask[i, j] = 1 / (1 + (dist / D0**2)**n)  # Formula del filtro pasa-bajos Butterworth

    return mask

#* Version mas eficiente
def filter_PB_gaussiano(dft_img, sigma):
    """
    Filtro pasa-bajos Gaussiano.
    Recibe la TDF y la desviacion estandar (sigma), para calcular la varianza.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    x = np.arange(-cols//2, cols//2)
    y = np.arange(-rows//2, rows//2)
    xx, yy = np.meshgrid(x, y)
    mask_2D = np.exp(-((xx**2 + yy**2) / (2 * sigma**2)))  # Formula del filtro pasa-bajos Gaussiano

    # Crear una mascara 3D con la misma forma que dft_img
    mask = np.zeros_like(dft_img)
    mask[:, :, 0] = mask_2D  # Llenar la primera capa de la mascara con mask_2D
    mask[:, :, 1] = mask_2D  # Llenar la segunda capa de la mascara con mask_2D
    return mask

#* Version con doble for
def filter_PB_gaussiano_v2(dft_img, sigma):
    """
    Filtro pasa-bajos Gaussiano.
    Recibe la TDF y la desviacion estandar (sigma), para calcular la varianza.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.zeros((rows, cols, 2), np.float32)

    for i in range(rows):
        for j in range(cols):
            dist = (i - crow)**2 + (j - ccol)**2  # Distancia al centro
            mask[i, j] = np.exp(-dist / (2 * sigma**2))  # Formula del filtro pasa-bajos Gaussiano

    return mask