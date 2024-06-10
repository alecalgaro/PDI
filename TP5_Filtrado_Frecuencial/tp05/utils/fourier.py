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


def FFT_stuff(img):
    fshift = np.fft.fftshift(np.fft.fft2(img))
    mag_img = np.abs(fshift)
    log_mag_img = 20*np.log(mag_img+0.000000001)
    img_new = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift)))
    img_new = cv2.normalize(img_new,None,0,255,cv2.NORM_MINMAX)
    return mag_img.astype("uint8"),log_mag_img,img_new


def get_pad_width(shape): #esto es por que si la imagen no es cuadrada no anda bien
    a = b = c = d = 0
    xx,yy = shape[0],shape[1]
    if (xx>yy):
        if (xx%2 == 0):
            b = 1
            xx = xx + 1
        dif = xx - yy
        c = d = int(dif/2)
        if (dif%2 != 0):
            d = d + 1
    else:
        if (yy > xx):
            if (yy%2 == 0):
                d = 1
                yy = yy + 1
            dif = yy - xx
            a = b = int(dif/2)
            if (dif%2 != 0):
                b = b + 1
        else:
            a = c = 1
    return ((a,b),(c,d))


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
        fsp[:,:,0]*=params["B"]
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


def homomorphic_filter(image, D, n=2, high_h=100, low_h=30):
    """TODO: Docstring for homomorphic_filter.

    Parameters:
        image: TODO
        D: TODO
        n: TODO
        high_h: TODO
        low_h: TODO
    Returns:
        TODO

    """
    #-------------------------------------------------------------------#
    # Homomorphic filtering
    #
    # image -> ln -> FFT -> H(Butterw filter) -> IFFT -> exp -> result
    #-------------------------------------------------------------------#

    # log
    img_log = np.log(image + 0.000001)

    # fft and shift of img_log
    img_fft = cv2.dft(np.float32(img_log)/255.0,flags=cv2.DFT_COMPLEX_OUTPUT)
    img_sfft = np.fft.fftshift(img_fft)

    # generate H(u, v)
    du = np.zeros(img_sfft.shape, dtype = np.float32)
    uu,vv,_ = img_sfft.shape
    for u in range(uu):
        for v in range(vv):
            du[u,v]=np.sqrt((u-uu/2.0)*(u-uu/2.0)+(v-vv/2.0)*(v-vv/2.0))

    du2 = cv2.multiply(du,du) / (D*D)
    re = np.exp(- n * du2)
    H = (high_h - low_h) * (1 - re) + low_h

    # apply H
    img_fltrd = cv2.mulSpectrums(img_sfft, np.float32(H), 0)

    # de-shift and ifft
    img_flog = np.fft.ifftshift(img_fltrd)
    img_flog = cv2.idft(img_flog)

    # normalization
    img_flog = cv2.magnitude(img_flog[:, :, 0], img_flog[:, :, 1])
    cv2.normalize(img_flog, img_flog, 0, 1, cv2.NORM_MINMAX)

    # exp and normalization
    img_final = np.exp(img_flog)
    cv2.normalize(img_final, img_final,0, 255, cv2.NORM_MINMAX)

    return img_final.astype("uint8")
