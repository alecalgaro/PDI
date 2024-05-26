import cv2
import numpy as np


def extraerSegmento(X1, Y1, X2, Y2, channel):
    """TODO: Docstring for extraerSegmento.

    Parameters:
        X1: TODO
        Y1: TODO
        X2: TODO
        Y2: TODO
        channel: TODO
    Returns:
        TODO

    """
    if X1==X2 and Y1==Y2:
        return channel[X1, Y1]
    if X1==X2:
        return channel[Y1:Y2, X1]
    if Y1==Y2:
        return channel[Y1, X1:X2]
    Y = [int(X*(Y2-Y1)//(X2-X1)+Y1) for X in range(X2-X1)]
    X = [i for i in range(X1,X2)]
    return channel[Y,X]


def obtenerPerfiles(imagen, modo, row=None, col=None, seg=None):
    """TODO: Docstring for obtenerPerfiles.

    Parameters:
        imagen: TODO
        modo: TODO
        row: TODO
        col: TODO
        seg: TODO
    Returns:
        TODO

    """
    assert ((row is not None) or (col is not None) or
            (seg is not None)), "Se debe seleccionar fila, columna o segmento"
    assert (((row is not None) ^ (col is not None))  ^ (seg is not None)
            ), "Se debe proporcionar fila o columna o segmento (no mas de 1)"
    assert not((row is not None) and (col is not None) and (seg is not None)
            ), "Se debe proporcionar fila o columna o segmento (no 3)"
    if modo=="Grises":
        if len(imagen.shape)>2:
            imagen=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        if seg is not None:
            return extraerSegmento(seg[0][0], seg[0][1], seg[1][0], seg[1][1],
                                   imagen)
        elif row is not None:
            return imagen[row,:]
        else:
            return imagen[:,col]

    perfiles=[]
    for ch in range(imagen.shape[2]):
        if seg is not None:
            perfiles.append(extraerSegmento(seg[0][0], seg[0][1], seg[1][0],
                                            seg[1][1], imagen[:,:,ch]))
        elif row is not None:
            perfiles.append(imagen[row,:,ch])
        else:
            perfiles.append(imagen[:,col,ch])

    return perfiles

