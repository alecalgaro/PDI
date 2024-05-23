import numpy as np

def add_impulsive_noise(img, noise_param=0.3, noise_type='bimodal', salt=False):
    """
    Agrega ruido impulsivo a una imagen.

    Parametros:
    - img: imagen de entrada.
    - noise_param: probabilidad de que un px sea afectado por el ruido impulsivo.
    - noise_type: 'unimodal' o 'bimodal'.
    - salt: True si el ruido es sal, False si es pimienta (si se usa 'unimodal')

    Salida:
    - img_noised: imagen con ruido impulsivo.
    """
    if(noise_type == "unimodal"):
        # Agregar ruido impulsivo unimodal (solo sal o solo pimienta, 255 o 0)
        img_noised = img.copy()
        mask = np.random.rand(*img.shape) < noise_param
        img_noised[mask] = 255 if salt else 0
    else:
        # Agregar ruido impulsivo bimodal (sal y pimienta)
        img_noised = img.copy()
        img_noised[np.random.rand(*img_noised.shape) < noise_param] = 0
        img_noised[np.random.rand(*img_noised.shape) < noise_param] = 255
    return img_noised