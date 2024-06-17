import cv2
import numpy as np
from skimage.util.shape import view_as_windows
from scipy.stats.mstats import gmean, hmean
from scipy.stats import trim_mean

###############################################################################
#                                Adding noise                                 #
###############################################################################

def add_impulsive_noise(image, Pa=0.1, Pb=0.1, A=0, B=255):
    """TODO: Docstring for add_impulsive_noise.

    Parameters:
        image: TODO
        Pa: TODO
        Pb: TODO
        A: TODO
        B: TODO
    Returns:
        TODO

    """
    row, col = image.shape
    img_n = image.copy()
    n_rand = np.random.rand(row,col)
    for x in range(row):
        for y in range(col):
            if n_rand[x,y] <= Pa:
                img_n[x,y] = A #--> Pepper
            elif n_rand[x,y] <= Pa+Pb:
                img_n[x,y] = B #--> Salt
    return img_n


def add_gaussian_noise(image, mean=0, stddev=1):
    """TODO: Docstring for add_gaussian_noise.

    Parameters:
        image: TODO
        mean: TODO
        stddev: TODO
    Returns:
        TODO

    """
    row, col = image.shape
    noise = np.zeros((row,col))
    noise = cv2.randn(noise, mean, stddev) #--> Gaussian distribution
    img_n = image.copy().astype("float") + noise
    #img_n = image.copy() + noise
    return img_n.astype("uint8")


def add_uniform_noise(image, A=108, B=148):
    """TODO: Docstring for add_uniform_noise.

    Parameters:
        image: TODO
        A: TODO
        B: TODO
    Returns:
        TODO

    """
    row, col = image.shape
    noise = np.zeros((row,col))
    noise = cv2.randu(noise, A, B) #--> Uniform distribution
    noise = noise - ((A+B)/2) #--> Convert to: Mean = 0
    img_n = image.copy().astype("float") + noise
    img_n = cv2.normalize(img_n,None,0,255,cv2.NORM_MINMAX)
    return img_n.astype("uint8")


def add_exponential_noise(image, a=0.05):
    """TODO: Docstring for add_exponential_noise.

    Parameters:
        image: TODO
        a: TODO
    Returns:
        TODO

    """
    row, col = image.shape
    noise = np.zeros((row,col))
    noise = np.random.exponential(1/a, [row,col])
    img_n = image.copy() + noise
    return img_n.astype("uint8")

###############################################################################
#                                Mean filters                                 #
###############################################################################

def windowize(image, m):
    """TODO: Docstring for windowize.

    Parameters:
        image: TODO
        m: TODO
    Returns:
        TODO

    """
    row, col = image.shape
    pad = m//2
    img_padded = cv2.copyMakeBorder(image, *[pad]*4, cv2.BORDER_REFLECT_101)
    img_windows = view_as_windows(img_padded, (m,m)) #--> split in windows
    return img_windows


def geometric_mean_filter(image, m=3):
    """TODO: Docstring for geometric_mean_filter.

    Parameters:
        image: TODO
        m: TODO
    Returns:
        TODO

    """
    img_windows = windowize(image,m) #--> split in windows
    img_f = gmean(img_windows+0.0000001, axis=(2,3))
    if m%2==0:
        img_f=img_f[0:-1,0:-1]
    return img_f.astype("uint8")


def contraharmonic_mean_filter(image, m=3, Q=2):
    """TODO: Docstring for contraharmonic_mean_filter.

    Parameters:
        image: TODO
        m: TODO
        Q: TODO
    Returns:
        TODO

    """
    img_windows = windowize(image,m) #--> split in windows
    top = np.sum(np.power(img_windows.astype('float32')+0.0000001, Q+1),
                 axis=(2,3))
    bottom = np.sum(np.power(img_windows.astype('float32')+0.0000001, Q),
                    axis=(2,3))
    img_f = top/bottom
    if m%2==0:
        img_f=img_f[0:-1,0:-1]
    return img_f.astype("uint8")

###############################################################################
#                                Order filters                                #
###############################################################################

def median_filter(image, m=3):
    """TODO: Docstring for median_filter.

    Parameters:
        image: TODO
        m: TODO
    Returns:
        TODO

    """
    img_windows = windowize(image,m) #--> split in windows
    img_f = np.median(img_windows, axis=(2,3))
    if m%2==0:
        img_f=img_f[0:-1,0:-1]
    return img_f.astype("uint8")


def midpoint_filter(image, m=3):
    """TODO: Docstring for midpoint_filter.

    Parameters:
        image: TODO
        m: TODO
    Returns:
        TODO

    """
    img_windows = windowize(image,m) #--> split in windows
    img_f=(np.max(img_windows.astype('float32'),
                  axis=(2,3)) + np.min(img_windows.astype('float32'),
                                       axis=(2,3)))/2
    if m%2==0:
        img_f=img_f[0:-1,0:-1]
    return img_f.astype("uint8")


def alpha_trimmed_mean_filter(image, m=3, d=2):
    """TODO: Docstring for alpha_trimmed_mean_filter.

    Parameters:
        image: TODO
        m: TODO
        d: TODO
    Returns:
        TODO

    """
    img_windows = windowize(image,m) #--> split in windows
    proportion = d/(m*m*2)
    w_row,w_col,_,_ = img_windows.shape
    img_windows = img_windows.reshape((w_row,w_col,m*m))
    img_f = trim_mean(img_windows,proportion,axis=2)
    if m%2==0:
        img_f=img_f[0:-1,0:-1]
    return img_f.astype("uint8")

###############################################################################
#                              Adaptative filter                              #
###############################################################################

def adaptative_local_filter(image, m=3, vn=5):
    """TODO: Docstring for adaptative_local_filter.

    Parameters:
        image: TODO
        m: TODO
        vn: TODO
    Returns:
        TODO

    """
    img_windows = windowize(image, m) #--> split in windows
    # Calculate mean and variance of every window
    W_mean = np.mean(img_windows.astype('float32'), axis=(2,3))
    W_var = np.var(img_windows.astype('float32'), axis=(2,3))+0.000000001
    # Fix inconsistencies
    aux = vn > W_var
    W_var[aux] = vn
    if m%2==0:
        W_mean=W_mean[0:-1,0:-1]
        W_var=W_var[0:-1,0:-1]

    img_f = image.astype("float32") - vn/W_var * (image - W_mean)
    img_f = cv2.normalize(img_f,None,0,255,cv2.NORM_MINMAX)
    return img_f.astype("uint8")

