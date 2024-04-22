"""
En este archivo ire dejando ejemplos de uso de las funciones que se proponen investigar
al comienzo del PDF de practica. En el word con anotaciones explico el funcionamiento 
y para que se usan.

Al final del listado de funciones en el PDF, dice:
En OpenCV.org recomiendan el uso de cv.dft() y cv.idft() porque son mas
rapidas que las de Numpy, sin embargo, las de Numpy son mas amigables.
"""

"""
dst = cv.dft(src[, dst[, flags[, nonzeroRows]]])

Se utiliza para realizar una Transformada Discreta de Fourier (DFT) en la imagen de entrada.

Parámetros:
- src: La imagen de entrada que se va a transformar. Debe ser una matriz de tipo flotante.
- dst (opcional): La imagen de salida que contiene la transformada. Si se proporciona, debe tener 
el mismo tamaño y tipo que src.
- flags (opcional): Este parámetro puede ser una combinación de las siguientes banderas:
    cv2.DFT_INVERSE: Realiza una Transformada Inversa de Fourier, es decir, convierte una imagen 
    del dominio de la frecuencia al dominio espacial.
    cv2.DFT_SCALE: Escala el resultado: divide el resultado por el número de elementos de la matriz.
    cv2.DFT_ROWS: Realiza una transformada en cada fila individualmente.
    cv2.DFT_COMPLEX_OUTPUT: Cuando se utiliza este flag, la salida es una matriz compleja (tiene dos canales).
    cv2.DFT_REAL_OUTPUT: Cuando se utiliza este flag, la salida es una matriz real (tiene un solo canal).
- nonzeroRows (opcional): Número de filas no nulas en la matriz de entrada. Esto se utiliza para 
optimizar el cálculo de la DFT. Si el número de filas no nulas en la matriz de entrada es conocido, se puede proporcionar aquí para acelerar el cálculo.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar una imagen en escala de grises
img = cv2.imread("../images/cameraman.tif", 0)

# Convertir la imagen a float32
img_float32 = np.float32(img)

# Realizar la Transformada de Fourier
dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)

# Cambiar a la escala logarítmica
dft_shift = np.fft.fftshift(dft)
magnitude_spectrum = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])

# Normalizar el espectro de magnitud
magnitude_spectrum_normalized = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)

# Mostrar la imagen y el espectro de magnitud
cv2.imshow('image', img)
cv2.imshow('spectrum', magnitude_spectrum_normalized)
cv2.waitKey()

"""
dst = np.fft.fft2(src)
Igual que cv2.dft para obtener la Transformada de Fourier en 2D, pero con numpy.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

# Cargar una imagen en escala de grises
img = cv2.imread("../images/cameraman.tif", 0)

# Convertir la imagen a float32
img_float32 = np.float32(img)

# Realizar la Transformada de Fourier
dft = np.fft.fft2(img_float32)

# Centrar la TF
dft_shift = np.fft.fftshift(dft) 

# Calcular la magnitud del espectro
magnitude_spectrum = np.abs(dft_shift)

# Normalizar el espectro de magnitud
magnitude_spectrum_normalized = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)

# Mostrar la imagen y el espectro de magnitud
cv2.imshow('image', img)
cv2.imshow('spectrum', magnitude_spectrum_normalized)
cv2.waitKey()

"""
dst = numpy.fft.fftshift(x, axes=None)

Funcion para centrar el componente de frecuencia cero de la señal en el centro del espectro.

Inicialmente la TF tiene su origen en la esquina superior izquierda, pero para visualizarla 
correctamente es necesario llevar el origen al centro de la imagen.

Parametros:
- x: matriz de entrada. Puede ser una matriz unidimensional o multidimensional.
- axes (opcional): Los ejes sobre los que se realiza el cambio. Si no se proporciona, 
se realiza el cambio sobre todos los ejes.
"""

# Ya la use en los ejemplos anteriores.

"""
dst = numpy.fft.ifftshift(x, axes=None)

Se utiliza para deshacer el cambio que hace numpy.fft.fftshift(). Es decir, cambia la representación 
de la Transformada de Fourier de centrada en la frecuencia cero a cero-centrada nuevamente.

Es decir, se utiliza si se desea llevar el origen de la TF de nuevo a la esquina superior izquierda
luego de haber aplicado numpy.fft.fftshift().
"""

import numpy as np
import matplotlib.pyplot as plt

# Crear una señal
t = np.arange(400)
n = np.zeros((400,), dtype=complex)
n[40:60] = np.exp(1j*np.random.uniform(0, 2*np.pi, (20,)))
s = np.fft.ifft(n)

# Realizar la Transformada de Fourier
f = np.fft.fft(s)

# Cambiar el componente de frecuencia cero al centro
f_shifted = np.fft.fftshift(f)

# Deshacer el cambio
f_unshifted = np.fft.ifftshift(f_shifted)

# Verificar si f y f_unshifted son iguales
print(np.allclose(f, f_unshifted))  # Debería imprimir True

"""
dst = cv.magnitude( x, y[, magnitude])

Se utiliza para calcular la magnitud de vectores 2D.

La magnitud de un vector 2D se calcula como sqrt(x^2 + y^2). Esta función calcula la magnitud 
de cada par de elementos correspondientes en las matrices de entrada x e y y almacena los 
resultados en la matriz de salida magnitude.

Parámetros:
- x: Coordenadas x de los vectores de entrada. Debe ser una matriz de tipo flotante.
- y: Coordenadas y de los vectores de entrada. Debe ser una matriz de tipo flotante y 
tener el mismo tamaño que x.
- magnitude (opcional): La matriz de salida que contiene las magnitudes de los vectores. 
Si se proporciona, debe tener el mismo tamaño y tipo que x.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

# Crear una imagen de entrada
img = cv2.imread('../images/cameraman.tif', 0)

# Convertir la imagen a float32
img_float32 = np.float32(img)

# Realizar la Transformada de Fourier
dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)

# Calcular la magnitud del espectro
magnitude = cv2.magnitude(dft[:,:,0], dft[:,:,1])

# Normalizar la magnitud (esto lo agrego porque la imagen se mostraba toda blanca porque los 
# valores de magnitud se encontraban fuera del rango de visualizacion de cv2.imshow() segun copilot)
magnitude_normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

# Visualizar la magnitud del espectro
cv2.imshow('Magnitude', magnitude_normalized)
cv2.waitKey()

"""
Diferencia entre np.abs() y cv2.magnitude():
- np.abs(): Esta es una función de NumPy que se utiliza para calcular el valor absoluto de 
cada elemento en la matriz de entrada. Si la matriz de entrada es compleja, np.abs() devuelve la 
magnitud (o norma) de cada elemento.

- cv.magnitude(): Esta es una función de OpenCV que se utiliza para calcular la magnitud de los 
vectores 2D. Toma dos matrices de entrada que representan las componentes x e y de los vectores, 
y devuelve una matriz de la misma talla que las matrices de entrada que contiene la magnitud de cada vector.

Por lo tanto, aunque ambas funciones pueden utilizarse para calcular la magnitud, se utilizan en 
diferentes contextos y con diferentes tipos de entrada. np.abs() se utiliza con una sola matriz de 
entrada que puede ser real o compleja, mientras que cv.magnitude() se utiliza con dos matrices de 
entrada que representan las componentes x e y de los vectores 2D.

Entonces, dependiendo de como calculo la TF, puedo usar una u otra funcion para calcular la magnitud.

- cv2.dft(): esta función de OpenCV devuelve un resultado en forma de dos canales (dos matrices), 
uno para la parte real y otro para la parte imaginaria de la TF. Por lo tanto, para obtener el 
espectro de magnitud, se usa cv2.magnitude(), que toma dos matrices de entrada 
(las partes real e imaginaria) y calcula la magnitud.

- np.fft.fft2(): esta función de NumPy devuelve una matriz compleja como resultado, donde cada 
elemento de la matriz es un número complejo que tiene una parte real e imaginaria. 
Para obtener el espectro de magnitud, se puede usar np.abs(), que calcula la magnitud 
(o valor absoluto) de cada número complejo en la matriz.
"""

"""
dst = np.log(x)

Calcular el logaritmo natural de los elementos del array.
"""

import numpy as np

# Crear un array de entrada
x = np.array([1, np.e, np.e**2, 0])

# Calcular el logaritmo natural de los elementos del array
log_x = np.log(x)

print(log_x)
# Imprimirá [ 0. 1. 2. -inf], que son los logaritmos naturales de los elementos en el array x. 
# El logaritmo natural de 0 es -inf, lo que significa que el logaritmo de 0 está indefinido.
# Y el ln(e^a) = a

"""
dst = cv.idft(src[, dst[, flags[, nonzeroRows]]])

Se utiliza para realizar una Transformada Discreta Inversa de Fourier en la imagen de entrada,
para convertir una imagen del dominio frecuencial al dominio espacial nuevamente.

Parámetros:
- src: La imagen de entrada que se va a transformar. Debe ser una matriz de tipo flotante.
- dst (opcional): La imagen de salida que contiene la transformada. Si se proporciona, debe tener el mismo tamaño y tipo que src.
- flags (opcional): Este parámetro puede ser una combinación de las siguientes banderas:
    cv2.DFT_SCALE: Escala el resultado: divide el resultado por el número de elementos de la matriz.
    cv2.DFT_ROWS: Realiza una transformada en cada fila individualmente.
    cv2.DFT_COMPLEX_OUTPUT: Cuando se utiliza este flag, la salida es una matriz compleja (tiene dos canales).
    cv2.DFT_REAL_OUTPUT: Cuando se utiliza este flag, la salida es una matriz real (tiene un solo canal).
- nonzeroRows (opcional): Número de filas no nulas en la matriz de entrada. Esto se utiliza para optimizar el cálculo de la IDFT. Si el número de filas no nulas en la matriz de entrada es conocido, se puede proporcionar aquí para acelerar el cálculo.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

# Crear una imagen de entrada
img = cv2.imread('../images/cameraman.tif', 0)

# Convertir la imagen a float32
img_float32 = np.float32(img)

# Realizar la Transformada de Fourier
dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)

dft_shift = np.fft.ifftshift(dft)

# Calcular la Transformada Inversa de Fourier
img_back = cv2.idft(dft_shift)

"""
dst = np.fft.ifft2(src)

Igual que cv2.idft para obtener la Transformada Inversa de Fourier en 2D, pero con numpy.
Sería la inversa de np.fft.fft2().

Parametros:
- src: La matriz de entrada que se va a transformar. Debe ser una matriz 2D de tipo complejo.

Devuelve una matriz compleja del mismo tamaño que la matriz de entrada src. Esta matriz de salida 
representa la Transformada de Fourier Inversa de la imagen o señal de entrada.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

# Crear una imagen de entrada
img = cv2.imread('../images/cameraman.tif', 0)

# Convertir la imagen a float32
img_float32 = np.float32(img)

# Realizar la Transformada de Fourier
dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)

dft_shift = np.fft.ifftshift(dft)

# Calcular la Transformada Inversa de Fourier
img_back = np.fft.ifft2(dft_shift)

"""
val = cv.getOptimalDFTSize(vecsize)

Se utiliza para obtener el tamaño óptimo para calcular la Transformada Discreta de Fourier (DFT). 
Este tamaño óptimo puede mejorar significativamente la eficiencia de la computación de la DFT,
ya que se puede utilizar la transformada rápida de Fourier (se hace internamente, no es una 
funcion distinta).

Parámetros:
- vecsize: El tamaño del vector para el cual se está buscando el tamaño óptimo de DFT.

La función cv.getOptimalDFTSize() devuelve el tamaño óptimo para la DFT que es mayor o igual que 
vecsize. Este tamaño óptimo es tal que la DFT puede ser calculada de manera más eficiente. 
Los tamaños que son potencias de 2 son más eficientes para calcular la DFT ya que internamente usa
la transformada rápida de Fourier en esos casos.
"""

import cv2

# Obtener el tamaño óptimo para la DFT
size = cv2.getOptimalDFTSize(100)

print(size)  # Debería imprimir 128, que es el tamaño óptimo para calcular la DFT de un vector de tamaño 100.

""""
dst = cv.copyMakeBorder(src, top, bottom, left, right, borderType[, dst[,value]])

Se utiliza para crear un borde alrededor de la imagen (o matriz) de entrada src.

Parametros:
- src: La imagen de entrada a la que se le va a añadir un borde.

- top, bottom, left, right: Indican cuántos píxeles de borde se añadirán a cada lado de la imagen.

- borderType: Define el tipo de borde que se va a añadir. Puede ser uno de los siguientes:
    cv.BORDER_CONSTANT: Añade un borde de color constante.
    cv.BORDER_REFLECT: El borde se llena reflejando la imagen sin incluir el último píxel. Por ejemplo, 'gfedcb|abcdefgh|gfedcba'
    cv.BORDER_REFLECT_101 o cv.BORDER_DEFAULT: Igual que cv.BORDER_REFLECT pero incluyendo el último píxel. Por ejemplo, 'gfedcb|abcdefghg|fedcba'
    cv.BORDER_REPLICATE: El borde se llena replicando el último píxel. Por ejemplo, 'aaaaaa|abcdefgh|hhhhhhh'
    cv.BORDER_WRAP: No se puede explicar con palabras, pero es similar a 'cdefgh|abcdefgh|abcdefg'

- dst (opcional): La imagen de salida con el borde añadido. Si se proporciona, debe tener el tamaño adecuado.

- value (opcional): Color del borde si el tipo de borde es cv.BORDER_CONSTANT. Es un valor escalar.

Devuelve una imagen que es la imagen de entrada src con un borde añadido.
"""

src = cv2.imread("../images/cameraman.tif")

# Crear un borde constante de 10 pixeles de color azul ([255, 0, 0] en BGR)
dst = cv2.copyMakeBorder(src, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 0, 0])

# Mostrar la imagen original y la imagen con borde
cv2.imshow('Original', src)
cv2.imshow('Bordered', dst)

"""
dst = cv.normalize(src, dst[, alpha[, beta[, norm type[, dtype[, mask]]]]])

Se utiliza para normalizar la imagen (o matriz) de entrada src.

Parámetros:
- src: La imagen de entrada que se va a normalizar.

- dst (opcional): La imagen de salida normalizada. Si se proporciona, debe tener el tamaño adecuado.

- alpha (opcional): El valor mínimo en el rango de normalización. Por defecto es 0.

- beta (opcional): El valor máximo en el rango de normalización. Por defecto es 255.

- norm_type (opcional): El tipo de normalización. Puede ser uno de los siguientes:
    cv.NORM_INF: El valor absoluto máximo de src se escala al valor especificado por beta.
    cv.NORM_L1: La suma de los valores absolutos de src se escala al valor especificado por beta.
    cv.NORM_L2: La raíz cuadrada de la suma de los cuadrados de src se escala al valor especificado por beta.
    cv.NORM_MINMAX: Los valores de src se escalan al rango especificado por alpha y beta.

- dtype (opcional): El tipo de datos de la imagen de salida dst. Si el valor es negativo, el tipo de datos de la imagen de salida es el mismo que el de la imagen de entrada.

- mask (opcional): Una máscara opcional que selecciona un subconjunto de la matriz para normalizar.

Devuelve una imagen que es la imagen de entrada src normalizada.
"""

# La use en las anteriores funciones para normalizar la magnitud del espectro de la imagen.

"""
magnitude, angle = cv.cartToPolar(x, y[, magnitude[, angle[, angleInDegrees]]])

Se utiliza para convertir las coordenadas cartesianas en coordenadas polares.

Parametros:

- x, y: Las componentes de los vectores de entrada. 
Estos son los valores de las coordenadas cartesianas.

- magnitude (opcional): La magnitud de los vectores de salida. 
Si se proporciona, debe tener el tamaño adecuado.

- angle (opcional): El ángulo de los vectores de salida, en radianes o grados dependiendo del 
valor de angleInDegrees. Si se proporciona, debe tener el tamaño adecuado.

- angleInDegrees (opcional): Un indicador booleano que especifica si los ángulos se deben dar 
en grados. Por defecto, los ángulos se dan en radianes.

Devuelve dos matrices que representan la magnitud y el ángulo de los vectores en las coordenadas polares.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

# Crear una imagen de entrada
img = cv2.imread('../images/cameraman.tif', 0)

# Convertir la imagen a float32
img_float32 = np.float32(img)

# Realizar la Transformada de Fourier
dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)

# Calcular la magnitud y el ángulo del espectro
magnitude, angle = cv2.cartToPolar(dft[:,:,0], dft[:,:,1])

"""
x, y = cv.polarToCart(magnitude, angle[, x[, y[, angleInDegrees]]])

Se utiliza para convertir las coordenadas polares en coordenadas cartesianas. 
Es la operación inversa de cv.cartToPolar().

Parametros:
- magnitude, angle: Las componentes de los vectores de entrada. 
Estos son los valores de las coordenadas polares.
- x, y (opcional): Las componentes de los vectores de salida. 
Si se proporcionan, deben tener el tamaño adecuado.
- angleInDegrees (opcional): Un indicador booleano que especifica si los ángulos están en grados. 
Por defecto, los ángulos están en radianes.

Devuelve dos matrices que representan las componentes x e y de los vectores en las coordenadas cartesianas.
"""

# Seria lo opuesto a cv.cartToPolar()

"""
dst = cv.mulSpectrums(a, b, flags[, c[, conjB]])

Se utiliza para realizar la multiplicación de dos espectros de Fourier en el dominio de la frecuencia.

Parametros:
- a, b: Las matrices de entrada que representan los espectros de Fourier. 
Estas deben ser de la misma talla y tipo.

- flags: Un indicador que puede ser cv.DFT_ROWS o cv.DFT_COMPLEX_OUTPUT.

- c (opcional): La matriz de salida de la misma talla y tipo que a.

- conjB (opcional): Un indicador booleano que especifica si el espectro b debe ser conjugado antes de la multiplicación.

Devuelve una matriz que es el resultado de la multiplicación de los dos espectros de Fourier de 
entrada. Esta matriz puede ser utilizada para realizar operaciones en el dominio de la frecuencia, 
como la filtración en el dominio de la frecuencia.
"""

import numpy as np
import cv2 as cv

# Crear dos matrices de entrada
a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)
b = np.array([[7, 8, 9], [10, 11, 12]], dtype=np.float32)

# Calcular la Transformada de Fourier de las matrices
dft_a = cv.dft(a, flags=cv.DFT_COMPLEX_OUTPUT)
dft_b = cv.dft(b, flags=cv.DFT_COMPLEX_OUTPUT)

# Multiplicar los espectros
mul_ab = cv.mulSpectrums(dft_a, dft_b, flags=cv.DFT_ROWS)

# Calcular la Transformada de Fourier inversa para obtener la matriz de salida
c = cv.idft(mul_ab, flags=cv.DFT_SCALE | cv.DFT_REAL_OUTPUT)

print(c)

"""
t = timeit.default_timer()

Se utiliza para medir el tiempo de ejecución de pequeños fragmentos de código. Esta función 
proporciona la hora actual en segundos desde algún punto de referencia, como el inicio del
sistema, la época, etc.

Es de la biblioteca timeit, que es una biblioteca estandar de Python, asi que no se debe instalar,
simplemente se importa como: import timeit
"""

import timeit

# Iniciar el temporizador
t_start = timeit.default_timer()

# Código cuyo tiempo de ejecución quieres medir
for i in range(1000000):
    pass

# Detener el temporizador
t_end = timeit.default_timer()

# Calcular y mostrar el tiempo de ejecución
print(f"Tiempo de ejecucion: {t_end - t_start} segundos")