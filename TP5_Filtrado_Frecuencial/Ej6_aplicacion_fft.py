import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import timeit

PATH = "../images/"
IMAGE = "camaleon.tif"

img_original = cv2.imread(f"{PATH}{IMAGE}", cv2.IMREAD_GRAYSCALE)

"""
Cargue una imagen y obtenga el tamano optimo (para filas y columnas)
al cual debe llevar la imagen para el calculo de la FFT.
Utilizar la funcion cv2.getOptimalDFTSize()
"""

#* Obtener el tamano optimo
# La funcion getOptimalDFTSize() devuelve el tamano optimo para la DFT
rows_op = cv2.getOptimalDFTSize(img_original.shape[0]) 
cols_op = cv2.getOptimalDFTSize(img_original.shape[1])

print(f"Dimension original: {img_original.shape}")
print(f"Dimension optima: ({rows_op}, {cols_op})")

"""
A partir de la imagen original genere una de tamano optimo (Nopt x Mopt)
agregando ceros. Utilizar la funcion cv2.copyMakeBorder()
"""

Nopt = rows_op - img_original.shape[0]
Mopt = cols_op - img_original.shape[1]

#* Agregar ceros
img_opt = cv2.copyMakeBorder(img_original, 0, Nopt, 0, Mopt, cv2.BORDER_CONSTANT, value=0)

cv2.imshow("Imagen optima", img_opt)

"""
Genere una imagen cuyo tamano en filas y columnas sea 1px menor al
tamano optimo ((Nopt - 1) x (Mopt - 1)) agregando ceros.
"""

Nopt -= 1 if Nopt > 1 else 0
Mopt -= 1 if Mopt > 1 else 0
img_no_opt = cv2.copyMakeBorder(img_original, 0, Nopt, 0, Mopt, cv2.BORDER_CONSTANT, value=0)

cv2.imshow("Imagen no optima", img_no_opt)

"""
Calcule la TDF de las 3 imagenes, visualice las magnitudes de las TDFs
y saque conclusiones, evalue el tiempo de computo de cada una.
"""

#* Calcular la TDF para la imagen original
start = timeit.default_timer()
dft_original = cv2.dft(np.float32(img_original), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_original = np.fft.fftshift(dft_original)
magnitude_original = cv2.magnitude(dft_original[:,:,0], dft_original[:,:,1])
magnitude_original = np.log(magnitude_original + 1)
magnitude_original = cv2.normalize(magnitude_original, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
end = timeit.default_timer()
print(f"Tiempo de computo para la imagen original: {end - start} segundos")

#* Calcular la TDF para la imagen optima
start = timeit.default_timer()
dft_opt = cv2.dft(np.float32(img_opt), flags=cv2.DFT_COMPLEX_OUTPUT)    # TDF
dft_opt = np.fft.fftshift(dft_opt)  # Centrar la TDF
magnitude_opt = cv2.magnitude(dft_opt[:,:,0], dft_opt[:,:,1])   # Magnitud
magnitude_opt = np.log(magnitude_opt + 1)   # Aplicar log para visualizar mejor la magnitud
magnitude_opt = cv2.normalize(magnitude_opt, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)  # Normalizar
end = timeit.default_timer()
print(f"Tiempo de computo para la imagen optima: {end - start} segundos")

#* Calcular la TDF para la imagen no óptima
start = timeit.default_timer()
dft_no_opt = cv2.dft(np.float32(img_no_opt), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_no_opt = np.fft.fftshift(dft_no_opt)
magnitude_no_opt = cv2.magnitude(dft_no_opt[:,:,0], dft_no_opt[:,:,1])
magnitude_no_opt = np.log(magnitude_no_opt + 1)
magnitude_no_opt = cv2.normalize(magnitude_no_opt, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
end = timeit.default_timer()
print(f"Tiempo de computo para la imagen no optima: {end - start} segundos")

#* Mostrar las imagenes
cv2.imshow("Magnitud original", magnitude_original)
cv2.imshow("Magnitud optima", magnitude_opt)
cv2.imshow("Magnitud no optima", magnitude_no_opt)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
¿Que efecto numerico (objetivo) y a la vista (subjetivo) produce el agregado de ceros?
"""