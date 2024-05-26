import cv2
import numpy as np


def get_dft(imagen, optimal=True, normalizar=True, imin=0, imax=255):
    """TODO: Docstring for get_dft.

    Parameters:
        imagen: TODO
        optimal: TODO
        normalizar: TODO
    Returns:
        TODO

    """
    rows, cols = imagen.shape
    if optimal:
        m = cv2.getOptimalDFTSize(rows)
        n = cv2.getOptimalDFTSize(cols)
        padded = cv2.copyMakeBorder(imagen, 0, m-rows, 0, n-cols,
                                    cv2.BORDER_CONSTANT, value=[0,0,0])
    else:
        m, n=rows, cols
        padded = np.copy(imagen)

    planes = [np.float32(padded), np.zeros(padded.shape, np.float32)]
    comp_img = cv2.merge(planes)
    comp_img = cv2.dft(np.float32(comp_img), flags=cv2.DFT_COMPLEX_OUTPUT)
    comp_img_sh = np.fft.fftshift(comp_img)

    mag_img, phi_img = cv2.cartToPolar(comp_img_sh[:,:,0], comp_img_sh[:,:,1])

    matOfOnes = np.ones(mag_img.shape, dtype=mag_img.dtype)
    cv2.add(matOfOnes, mag_img, mag_img)
    cv2.log(mag_img, mag_img)

    if normalizar:
        cv2.normalize(mag_img, mag_img, imin, imax, cv2.NORM_MINMAX)
        cv2.normalize(phi_img, phi_img, imin, imax, cv2.NORM_MINMAX)

    mag_img=mag_img.astype("uint8")
    phi_img=phi_img.astype("uint8")
    return mag_img, phi_img, comp_img_sh


def get_idft(comp_img_sh, normalizar=True, imin=0, imax=255):
    """TODO: Docstring for get_idft.

    Parameters:
        comp_img_sh: TODO
    Returns:
        TODO

    """
    comp_img = np.fft.ifftshift(comp_img_sh)
    img_back = cv2.idft(comp_img)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

    if normalizar:
        cv2.normalize(img_back, img_back, imin, imax, cv2.NORM_MINMAX)

    img_back=img_back.astype("uint8")
    return img_back


###############################################################################
#                                  Filtrado                                   #
###############################################################################
IDEAL_FILTER, BUTTERWORTH_FILTER, GAUSSIAN_FILTER = 0, 1, 2

def apply_filter(img, fil_type, params, is_lowpass, is_high_boost=False):
    """TODO: Docstring for apply_filter.

    Parameters:
        img: TODO
        fil_type: TODO
        params: TODO
        is_lowpass: TODO
        is_high_boost: TODO
    Returns:
        TODO

    """
    _,_,imgsp = get_dft(img)

    if fil_type==IDEAL_FILTER:
        fmag = ideal_filter(imgsp.shape[:-1], params, is_lowpass)
    elif fil_type==BUTTERWORTH_FILTER:
        fmag = butterworth_filter(imgsp.shape[:-1], params, is_lowpass)
    elif fil_type==GAUSSIAN_FILTER:
        fmag = gaussian_filter(imgsp.shape[:-1], params, is_lowpass)

    fsp = np.zeros_like(imgsp)
    fsp[:,:,0]=fmag
    if is_high_boost:
        fsp[:,:,0]+=params["A"]-1
    imgsp = cv2.mulSpectrums(imgsp, fsp, cv2.DFT_ROWS)
    return get_idft(imgsp)


def ideal_filter(img_shape, params, is_lowpass):
    """TODO: Docstring for ideal_filter.

    Parameters:
        img_shape: TODO
        params: TODO
        is_lowpass: TODO
    Returns:
        TODO

    """
    limit = params["R0"]**2
    mag = np.zeros(img_shape)
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            dist = (i-img_shape[0]//2)**2+(j-img_shape[1]//2)**2
            if is_lowpass:
                mag[i,j]=1 if dist<limit else 0
            else:
                mag[i,j]=1 if dist>=limit else 0

    return mag


def butterworth_filter(img_shape, params, is_lowpass):
    """TODO: Docstring for ideal_filter.

    Parameters:
        img_shape: TODO
        params: TODO
        is_lowpass: TODO
    Returns:
        TODO

    """
    mag, R0, N = np.zeros(img_shape), params["R0"], params["n"]
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            dist = (i-img_shape[0]//2)**2+(j-img_shape[1]//2)**2
            if is_lowpass:
                mag[i,j]=1/(1+(dist/(R0**2))**N)
            else:
                mag[i,j]=1/(1+((R0**2)/dist)**N) if dist>0 else 0

    return mag


def gaussian_filter(img_shape, params, is_lowpass):
    """TODO: Docstring for ideal_filter.

    Parameters:
        img_shape: TODO
        params: TODO
        is_lowpass: TODO
    Returns:
        TODO

    """
    mag, sigma = np.zeros(img_shape), params["sigma"]
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            dist = (i-img_shape[0]//2)**2+(j-img_shape[1]//2)**2
            if is_lowpass:
                mag[i,j]=np.exp(-dist/(2*(sigma**2)))
            else:
                mag[i,j]=1-np.exp(-dist/(2*(sigma**2)))

    return mag


