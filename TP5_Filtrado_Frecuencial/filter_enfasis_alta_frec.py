import frequency_filters_PA as f_PA

def filter_enfasis_alta_frec(dft_img, a, b, sigma):
    """
    Funcion que genera un filtro de enfasis de alta frecuencia.
    Recibe la DTF de la imagen, los parametros a y b, siendo a >= 0 y
    b > a, ademas de sigma para usar con el filtro PA gaussiano.
    """
    mask = a + b*f_PA.filter_PA_gaussiano_v2(dft_img, sigma)
    return mask