import numpy as np

#? ------------------------ FILTROS PASA-ALTOS EN FRECUENCIA ------------------------
# Son lo opuesto a los filtros pasa-bajos en frecuencia.

# Filtro pasa-altos ideal en frecuencia.
# Matriz de unos, del mismo tamaño que la imagen.
# Desde el centro, se crea un circulo de radio D0 (frecuencia de corte), y dentro de ese 
# circulo se pone todo 0.

# Al recibir la dft, se toman solo las dos primeras dimensiones [:2] porque la dft tiene
# una dimension mas para la parte real y la imaginaria pero no nos interesa al aplicar el filtro.

def filter_PA_ideal(dft, D0):
    """
    Funcion que crea un filtro pasa-bajos ideal.
    Recibe la TDF y la frecuencia de corte D0 (radio del circulo).
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.ones((rows, cols, 2), np.float32)
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - crow)**2 + (y - ccol)**2 <= D0**2
    mask[mask_area] = 0  # Circulo de radio D0 centrado en el centro y con todo 0
    return mask

#* Version del PA ideal con doble for
def filter_PA_ideal_v2(dft, D0):
    """
    Funcion que crea un filtro pasa-bajos ideal.
    Recibe la TDF y la frecuencia de corte D0 (radio del circulo).
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    mask = np.ones_like(dft)   # Mascara de unos del mismo tamaño que la TDF
    rows, cols = dft.shape[:2]  # Filas y columnas de la TDF
    center = (rows//2, cols//2)  # Centro de la TDF
    # Si la distancia desde el punto (u,v) al centro es menor a D0, se pone 0
    for u in range(rows):
        for v in range(cols):
            if np.sqrt((u-center[0])**2 + (v-center[1])**2) <= D0:
                mask[u,v] = 0
    return mask

#* Version mas eficiente
def filter_PA_butterworth(dft_img, D0, n):
    """
    Filtro pasa-altos Butterworth de orden "n".
    Recibe la TDF, la frecuencia de corte D0 y el orden del filtro.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    x = np.arange(-cols//2, cols//2)
    y = np.arange(-rows//2, rows//2)
    xx, yy = np.meshgrid(x, y)
    mask_2D = 1 / (1 + (D0 / np.sqrt(xx**2 + yy**2))**(2*n))    # Formula del filtro pasa-bajos Butterworth

    # Crear una mascara 3D con la misma forma que dft_img
    mask = np.zeros_like(dft_img)
    mask[:, :, 0] = mask_2D  # Llenar la primera capa de la mascara con mask_2D
    mask[:, :, 1] = mask_2D  # Llenar la segunda capa de la mascara con mask_2D
    return mask

#* Version con doble for pero sin raiz cuadrada
# Para evitar usar la raiz cuadrada, se modifica la formula del filtro Butterworth
# usando 1 / (1 + (D(u,v) / D0^2)^n)
def filter_PA_butterworth_v2(dft_img, D0, n):
    """
    Filtro pasa-altos Butterworth de orden "n".
    Recibe la TDF, la frecuencia de corte D0 y el orden del filtro.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.zeros((rows, cols, 2), np.float32)

    for i in range(rows):
        for j in range(cols):
            dist = (i - crow)**2 + (j - ccol)**2  # Distancia al centro
            if(dist == 0): # Evitar division por cero
                mask[i, j] = 0
            else:
                mask[i, j] = 1 / (1 + (D0**2 / dist)**n)  # Formula del filtro pasa-bajos Butterworth

    return mask

#* Version con doble for
def filter_PA_gaussiano_v2(dft_img, sigma):
    """
    Filtro pasa-altos Gaussiano.
    Recibe la TDF y la desviacion estandar (sigma), para calcular la varianza.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.zeros((rows, cols, 2), np.float32)

    for i in range(rows):
        for j in range(cols):
            dist = (i - crow)**2 + (j - ccol)**2  # Distancia al centro
            mask[i, j] = 1 - np.exp(-dist / (2 * sigma**2))  # Formula del filtro pasa-bajos Gaussiano

    return mask