import numpy as np

def add_gaussian_noise(img, noise_param=0.1):
    """
    Agrega ruido gaussiano a una imagen.

    Parametros:
    - img: imagen de entrada.
    - noise_param: desvio estandar del ruido gaussiano.

    Salida:
    - img_noised: imagen con ruido gaussiano.
    """
    img_noised = img + noise_param * np.random.randn(*img.shape)
    img_noised = np.clip(img_noised, 0, 255).astype(np.uint8)
    return img_noised