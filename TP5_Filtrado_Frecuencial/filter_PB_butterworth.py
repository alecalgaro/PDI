import numpy as np

def create_filter_PB_butterworth(dft_img, D0, n):
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

#* Version con doble for, menos eficiente, asi que en caso de usar trackbars no es una buena
#* opcion porque debe hacer muchos calculos. Si se usa con un solo valor de D0 y "n" no hay problema
def create_filter_PB_butterworth_v2(dft_img, D0, n):
    """
    Filtro pasa-bajos Butterworth de orden "n".
    Recibe la TDF, la frecuencia de corte D0 y el orden del filtro.
    Devuelve la mascara del filtro para multiplicar con la TDF.
    """
    rows, cols = dft_img.shape[:2]
    crow, ccol = rows//2, cols//2   # Centro de la TDF
    mask = np.zeros((rows, cols, 2), np.uint8)

    for i in range(rows):
        for j in range(cols):
            dist = np.sqrt((i - crow)**2 + (j - ccol)**2)  # Distancia al centro
            mask[i, j] = 1 / (1 + (dist / D0)**(2*n))  # Formula del filtro pasa-bajos Butterworth

    return mask