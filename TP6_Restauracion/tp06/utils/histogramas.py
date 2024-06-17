import cv2


def calcularHistograma(imagen, modo="Grises", mascara=None, bins=None,
                       rango=None):
    """TODO: Docstring for calcularHistograma.

    Parameters:
        imagen: TODO
        modo: TODO
        mascara: TODO
        bins: TODO
        rango: TODO
        256]: TODO
    Returns:
        TODO

    """
    if modo=="Grises":
        if bins is None:
            bins = 256
        if rango is None:
            rango=[0, 256]
        hist = cv2.calcHist([imagen], [0], mascara, [bins], rango)
    elif modo=="BGR":
        bgr_planes = cv2.split(imagen)
        if bins is None:
            bins = [256, 256, 256]
        if rango is None:
            rango=[[0, 256], [0, 256], [0, 256]]
        hist = [cv2.calcHist(bgr_planes, [0], mascara, [bins[0]], rango[0]),
                cv2.calcHist(bgr_planes, [1], mascara, [bins[1]], rango[1]),
                cv2.calcHist(bgr_planes, [2], mascara, [bins[2]], rango[2])]
    elif modo=="HSV":
        hsv_planes = cv2.split(imagen)
        if bins is None:
            bins = [181, 256, 256]
        if rango is None:
            rango=[[0, 181], [0, 256], [0, 256]]
        hist = [cv2.calcHist(hsv_planes, [0], mascara, [bins[0]], rango[0]),
                cv2.calcHist(hsv_planes, [1], mascara, [bins[1]], rango[1]),
                cv2.calcHist(hsv_planes, [2], mascara, [bins[2]], rango[2])]
    else:
        print("ERROR! Seleccione un modo valido")
    return hist


def equalizarHistograma(imagen, modo="Grises", canales=None):
    """TODO: Docstring for equalizarHistograma.

    Parameters:
        imagen: TODO
        modo: TODO
        canales: TODO
    Returns:
        TODO

    """
    if modo=="Grises":
        img_eq = cv2.equalizeHist(imagen)
    elif modo=="BGR" or modo=="HSV":
        planes = cv2.split(imagen)
        if canales is None:
            canales = [0, 1, 2]
        pln_eq = []
        for c in range(len(planes)):
            if c in canales:
                pln_eq.append(cv2.equalizeHist(planes[c]))
            else:
                pln_eq.append(planes[c])
        img_eq=cv2.merge(pln_eq)
    else:
        print("ERROR! Seleccione un modo valido")
    return img_eq


def media(hist):
    Prob = hist/sum(hist)
    mean = 0
    for g in range(hist.shape[0]):
        mean += g * Prob[g]
    return mean


def varianza(hist):
    Prob = hist/sum(hist)
    mean = media(hist)
    variance = 0
    for g in range(hist.shape[0]):
        variance += (g - mean)**2 * Prob[g]
    return variance


def asimetria(hist):
    Prob = hist/sum(hist)
    mean = media(hist)
    skewness = 0
    for g in range(hist.shape[0]):
        skewness += (g - mean)**3 * Prob[g]
    return skewness


def energia(hist):
    Prob = hist/sum(hist)
    energy = 0
    for g in range(hist.shape[0]):
        energy += Prob[g]**2
    return energy


def entropia(hist):
    Prob = hist/sum(hist)
    entropy = 0
    for g in range(hist.shape[0]):
        if Prob[g] != 0:
            entropy += -Prob[g] * np.log2(Prob[g])
    return entropy
