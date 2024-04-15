import numpy as np
import cv2

###############################################################################
#                             Funciones para tp04                             #
###############################################################################
def getComplementary(image):
    """TODO: Docstring for getComplementary.

    Parameters:
        image: TODO
    Returns:
        TODO

    """
    imhsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)#.astype("float")
    compl = np.copy(imhsv)
    compl[imhsv[:,:,0]<=90,0]=imhsv[imhsv[:,:,0]<=90,0]+90
    compl[imhsv[:,:,0]>90,0]=imhsv[imhsv[:,:,0]>90,0]-90
    return cv2.cvtColor(compl, cv2.COLOR_HSV2BGR)


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
    Y = [int(X*(Y2-Y1)/(X2-X1)+Y1) for X in range(X2-X1)]
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

###############################################################################
#                             Funciones para tp03                             #
###############################################################################
def generateKernel(method, size=(3,3)):
    """TODO: Docstring for generateKernel.

    Parameters:
        method: TODO
        size: TODO
    Returns:
        TODO

    """
    # Limitamos el tamano a numeros impares
    assert size[0]%2==1 and size[1]%2==1, "El kernel debe tener tamano impar"

    if method == "pbcaja":
        mask = np.ones(size, np.float32)/(size[0]*size[1])
    elif method == "pbcruz":
        mask = np.zeros(size, np.float32)
        mask[size[0]//2, :] = 1/(size[0]+size[1]-1)
        mask[:, size[1]//2] = 1/(size[0]+size[1]-1)
    elif method == "pacaja0":
        mask = -1*np.ones(size, np.float32)
        mask[size[0]//2, size[1]//2] = size[0]*size[1]-1
    elif method == "pacruz0":
        mask = np.zeros(size, np.float32)
        mask[size[0]//2, :] = -1
        mask[:, size[1]//2] = -1
        mask[size[0]//2, size[1]//2] = size[0]+size[1]-2
    elif method == "pacaja1":
        mask = -1*np.ones(size, np.float32)
        mask[size[0]//2, size[1]//2] = size[0]*size[1]
    elif method == "pacruz1":
        mask = np.zeros(size, np.float32)
        mask[size[0]//2, :] = -1
        mask[:, size[1]//2] = -1
        mask[size[0]//2, size[1]//2] = size[0]+size[1]-1
    else:
        print("Seleccione un metodo valido")

    return mask

###############################################################################
#                            Funciones para tp02a                             #
###############################################################################
#########
#  LUT  #
#########
def computeLUT(R, a, c, smin=0, smax=255, dtype="uint8"):
    """Aplicamos LUT dada la tabla de intensidades R y los coeficientes a y c.

    Parameters:
        R: Tabla de valores a mapear.
        a: Factor de ganancia.
        c: Offset.
        smin: Minimo a partir del cual se aceptan los valores resultantes. Por
        defecto es 0.
        smax: Maximo hasta el cual se aceptan los valores resultantes. Por
        defecto es 255.
        dtype: Tipo de dato de la imagen resultante ("uint8" por defecto)
    Returns:
        S: Tabla de intensidades resultante.

    """
    S = a*R.astype("float")+c
    S = np.clip(S, smin, smax)
    return S.astype(dtype)


def applyLUT(imagen, A, C, Rlims=[(0, 255)], rstep=1, smin=0, smax=255,
             dtype="uint8"):
    """Aplicamos LUT a la imagen dada. Se reciben los valores de los
    coeficientes en listas, para pasarse por tramos.

    Parameters:
        imagen: Imagen a transformar.
        A: Lista de factores de ganancia.
        C: Lista de offsets.
        Rlims: Lista de tuplas de la forma [(rmin1, rmax1), (rmin2, rmax2),
        ...] para determinar los limites de los tramos. Por defecto cubre todo
        el rango asi se hace un solo tramo.
        rstep: Paso para generar la tabla de intensidades. Por defecto es 1.
        smin: Minimo a partir del cual se aceptan los valores resultantes. Por
        defecto es 0.
        smax: Maximo hasta el cual se aceptan los valores resultantes. Por
        defecto es 255.
        dtype: Tipo de dato de la imagen resultante ("uint8" por defecto)
    Returns:
        new_image: Imagen resultante.

    """
    new_image = np.zeros_like(imagen, dtype=dtype)
    for i in range(len(Rlims)):
        if Rlims[i][0] != Rlims[i][1]:
            R = np.arange(Rlims[i][0], Rlims[i][1]+rstep, rstep, dtype=dtype)
            S = computeLUT(R, A[i], C[i], smin, smax, dtype)
            for j in range(len(R)):
                new_image[imagen==R[j]] = S[j]
    return new_image


def applyNegative(imagen):
    """Aplicamos el negativo (simplemente llamamos a applyLUT pero con los
    parametros adecuados)

    Parameters:
        imagen: Imagen a transformar.
    Returns:
        new_image: Imagen resultante.

    """
    return applyLUT(imagen, [-1], [np.max(imagen)])


def plotLUT(ax, A, C, Rlims=[(0, 255)], rstep=1, rmin=0, rmax=255, smin=0,
            smax=255):
    """Graficamos el mapeo (es decir la recta de la funcion aplicada)

    Parameters:
        ax: Axis para graficar.
        A: Lista de factores de ganancia.
        C: Lista de offsets.
        Rlims: Lista de tuplas de la forma [(rmin1, rmax1), (rmin2, rmax2),
        ...] para determinar los limites de los tramos. Por defecto cubre todo
        el rango asi se hace un solo tramo.
        rstep: Paso para generar la tabla de intensidades. Por defecto es 1.
        rmin: Limite inferior en x. Por defecto es 0.
        rmax: Limite superior en x. Por defecto es 255.
        smin: Limite inferior en y. Por defecto es 0.
        smax: Limite superior en y. Por defecto es 255.
    Returns:
        ax: Axis modificados.

    """
    for i in range(len(Rlims)):
        if Rlims[i][0] != Rlims[i][1]:
            R = np.arange(Rlims[i][0], Rlims[i][1]+rstep, rstep)
            ax.plot(R, computeLUT(R, A[i], C[i], smin, smax), 'b-',
                    linewidth=2)
        else:
            # Esto dibuja linea vertical. Como A y C deben tener el mismo
            # tamano que Rlims, aprovecho esos lugares para saber desde donde
            # y hasta donde hacer la linea
            ax.plot([Rlims[i][0], Rlims[i][1]], [a[i], c[i]], 'b-',
                    linewidth=2)
    ax.set(xlim=(rmin, rmax+rstep), ylim=(smin, smax+rstep))
    return ax


def hacerTramos(points):
    """Recibe los puntos necesarios para generar los tramos de la LUT. Fija
    los puntos (0, 0) y (255, 255)

    Parameters:
        points: Lista de tuplas de la forma [(x1, y1), (x2, y2), ...] para
        determinar por donde pasa la funcion por tramos.
    Returns:
        A: Lista de factores de ganancia.
        C: Lista de offsets.
        Rlims: Lista de tuplas de la forma [(rmin1, rmax1), (rmin2, rmax2),
        ...] para determinar los limites de los tramos.

    """
    p0 = (0,0)
    A, C, Rlims = [], [], []
    for p in points:
        # TODO: Agregar linea vertical o warning si el denominador es 0 #
        if abs(p[0]-p0[0])>1e-3:
            a = (p[1]-p0[1])/(p[0]-p0[0])
            c = p[1]-a*p[0]
        else:
            # no deberian accederse nunca a estos valores, salvo para plot
            a, c = p0[1], p[1]
        A.append(a)
        C.append(c)
        Rlims.append((p0[0], p[0]))
        p0=p
    p=(255, 255)
    a = (p[1]-p0[1])/(p[0]-p0[0])
    c = p[1]-a*p[0]
    A.append(a)
    C.append(c)
    Rlims.append((p0[0], p[0]))
    return A, C, Rlims


#################
#  No lineales  #
#################
def computeLog(R, c=1, smin=0, smax=1, dtype="uint8"):
    """Aplicamos transformacion logaritmica a la entrada.

    Parameters:
        R: Tabla de valores (o imagen)
        c: Constante de escalado???
        dtype: Tipo de dato de la imagen resultante ("uint8" por defecto)
    Returns:
        S: Tabla de intensidades resultante.

    """
    if dtype=="uint8":
        R= R.astype("float")/255.0
    S = c*np.log(1.+R, dtype="float")
    S = np.clip(S, smin, smax)
    if dtype=="uint8":
        S*=255
    return S.astype(dtype)


def computePow(R, gamma, c=1, smin=0, smax=1., dtype="uint8"):
    """Aplicamos transformacion de potencia a la entrada.

    Parameters:
        R: Tabla de valores (o imagen)
        gamma: Exponente gamma.
        c: Constante de escalado???
        dtype: Tipo de dato de la imagen resultante ("uint8" por defecto)
    Returns:
        S: Tabla de intensidades resultante.

    """
    if dtype=="uint8":
        R= R.astype("float")/255.0
    S = c*np.power(R, gamma, dtype="float")
    S = np.clip(S, smin, smax)
    if dtype=="uint8":
        S*=255
    return S.astype(dtype)


#################
#  Aritmeticas  #
#################
def blending(img1, img2, a, imax=255, imin=0):
    """Aplicamos alpha blending dadas dos imagenes y el alpha.

    Parameters:
        img1: Primera imagen a sumar.
        img2: Segunda imagen a sumar.
        a: Valor de alpha.
        imin: Minimo a partir del cual se aceptan los valores resultantes. Por
        defecto es 0.
        imax: Maximo hasta el cual se aceptan los valores resultantes. Por
        defecto es 255.
    Returns:
        res: Imagen resultante.

    """
    img = (1-a)*img1+a*img2
    img = np.clip(img, imin, imax)
    return img


def suma_promedio(imgs, imin=0, imax=255, dtype="uint8"):
    """Calculamos el promedio de varias imagenes.

    Parameters:
        imgs: Lista de imagenes a promediar.
        imin: Minimo a partir del cual se aceptan los valores resultantes. Por
        defecto es 0.
        imax: Maximo hasta el cual se aceptan los valores resultantes. Por
        defecto es 255.
        dtype: Tipo de dato de la imagen resultante ("uint8" por defecto)
    Returns:
        img: Imagen resultante.

    """
    img = imgs[0].astype("float")
    for i in range(1, len(imgs)):
        img += imgs[i].astype("float")

    img /= len(imgs)
    img = np.clip(img, imin, imax)
    return img.astype(dtype)


def diferencia(img1, img2, reesc="sum", imin=0, imax=255, dtype="uint8"):
    """Calculamos la resta de dos imagenes y reescalamos aplicando el metodo
    seleccionado.

    Parameters:
        img1: Primera imagen a restar.
        img2: Segunda imagen a restar.
        reesc: Metodo de reescalado. Si es "sum", suma 255 y divide por 2. Si
        es "res", resta el minimo y escala a 255 ("sum" por defecto)
        dtype: Tipo de dato de la imagen resultante ("uint8" por defecto)
    Returns:
        img: Imagen resultante.

    """
    img1=img1.astype("float")
    img2=img2.astype("float")
    img = img1-img2
    if reesc == "sum":
        img = (img+255)/2
    elif reesc == "res":
        img = (img-img.min())*(255/(img.max()-img.min()))
    elif reesc == "no":
        img = np.clip(img, imin, imax)
    else:
        print("Error: elegir uno de los valores para reescalar: sum o res")
        return

    return img.astype(dtype)


def multiplicacion(img, mask, dtype="uint8"):
    """Multiplicamos una imagen por una mascara binaria.

    Parameters:
        img: Imagen a multiplicar.
        mask: Mascara binaria a aplicar.
        dtype: Tipo de dato de la imagen resultante ("uint8" por defecto)
    Returns:
        res: Imagen resultante.

    """
    img=img.astype("float")
    if np.max(mask)>1:
        mask = mask/np.max(mask)
    res = img*mask
    return res.astype(dtype)


###############################################################################
#                           Otras funciones utiles                            #
###############################################################################
def mse(img1, img2):
    """Error cuadratico medio entre dos imagenes.

    Parameters:
        img1: TODO
        img2: TODO
    Returns:
        TODO

    """
    img1=img1.astype("float")
    img2=img2.astype("float")
    return (np.square(img1 - img2)).mean(axis=None)


def extraerROIenmarcada(imagen, punto, umbral, es_inferior=True):
    """TODO: Docstring for extraerROIenmarcada.

    Parameters:
        imagen: TODO
        punto: TODO
        umbral: TODO
        es_superior: TODO
    Returns:
        TODO

    """
    print(imagen.shape)
    columna = obtenerPerfiles(imagen, "Grises", col=punto[0])
    print(len(columna))
    es_marco = columna[0]>umbral if es_inferior else columna[0]<umbral
    afuera = not es_marco
    ymin, ymax = 0, len(columna)-1
    for y in range(1, len(columna)):
        if not es_marco:
            if (columna[y]>umbral):# and es_inferior) or
                #(columna[y]<umbral and not es_inferior)):
                # No estabamos en marco entramos
                es_marco=True
                if not afuera:
                    # Estabamos dentro, salimos porque el marco cuenta como
                    # afuera. Marcamos el limite de la ROI
                    afuera=True
                    ymax=y
        else:
            if (columna[y]<umbral):# and es_inferior) or
                #(columna[y]>umbral and not es_inferior)):
                # Estabamos en marco y salimos
                es_marco=False
                if afuera:
                    # Estabamos afuera y como salimos del marco entramos en
                    # la ROI buscada
                    afuera=False
                    ymin=y

    fila = obtenerPerfiles(imagen, "Grises", row=punto[1])
    es_marco = fila[0]>umbral if es_inferior else fila[0]<umbral
    afuera = not es_marco
    xmin, xmax = 0, len(fila)-1
    for x in range(1, len(fila)):
        if not es_marco:
            if ((fila[x]>umbral and es_inferior) or
                (fila[x]<umbral and not es_inferior)):
                # No estabamos en marco entramos
                es_marco=True
                if not afuera:
                    # Estabamos dentro, salimos porque el marco cuenta como
                    # afuera. Marcamos el limite de la ROI
                    afuera=True
                    xmax=x
        else:
            if ((fila[x]<umbral and es_inferior) or
                (fila[x]>umbral and not es_inferior)):
                # Estabamos en marco y salimos
                es_marco=False
                if afuera:
                    # Estabamos afuera y como salimos del marco entramos en
                    # la ROI buscada
                    afuera=False
                    xmin=x

    print(ymin, ymax, xmin, xmax)
    return ymin, ymax, xmin, xmax

