"""
 Cada funcion recibe un histograma y devuelve la propiedad estadistica correspondiente.
 
 Prob = hist/sum(hist)
 Es la probabilidad de cada nivel de gris 
 (numero de pixeles de ese nivel de gris dividido por el total de pixeles)
 
 Prob[g]    # Probabilidad de que un pixel tenga nivel de gris "g"
"""

import numpy as np

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

