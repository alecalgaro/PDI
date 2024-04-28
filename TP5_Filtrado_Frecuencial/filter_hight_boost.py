import frequency_filters_PA as f_PA

def filter_hight_boost(dft_img, A, sigma):
    """
    Funcion que devuelve el filtro de realce de alta frecuencia.
    Recibe la DFT de la imagen, el parametro A y el valor de sigma para 
    usar con el filtro PA gaussiano.
    """
    mask = (A-1) + f_PA.filter_PA_gaussiano_v2(dft_img, sigma)
    return mask