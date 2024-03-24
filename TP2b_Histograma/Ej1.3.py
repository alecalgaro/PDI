import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import matplotlib.pyplot as plt

"""
Ecualizacion de histograma.

La ecualizacion de histograma es una técnica que permite mejorar el contraste de una imagen (diferencia
entre gris minimo y gris maximo), y haciendo que el brillo medio quede más al centro.
 
Consiste en modificar la distribución de los niveles de gris de la imagen de manera que el histograma
de la imagen ecualizada sea lo más parecido a una distribución uniforme. 
En otras palabras, la ecualización o igualización redistributye los niveles de grises de la imagen
original sobre todo el rango de grises disponibles, para que todos los niveles de grises tengan la
misma probabilidad de aparición.

En la teoria (pág. 38) vimos un ejemplo con la imagen coins.tif donde dijimos que no siempre produce 
buenos resultados la ecualización, particularmente cuando el histograma original esta muy localizado
(pico), pudiendo producir falsos bordes y regiones de diferente intensidad. En esos casos tambien
aumenta la "granulosidad" de la imagen.
"""

"""
Se puede probar por ejemplo con las imagenes imagenA.tif, imagenB.tif, imagenC.tif, imagenD.tif 
e imagenE.tif que venimos usando, para ver las diferencias y tener casos donde el histograma
tiene más o menos picos, ver cuando es útil la ecualización y demás.

imagenB.tif e imagenE.tif son un buen ejemplo de un caso donde la ecualización mejora mucho la imagen.
Mientras que la imagen coins.tif es un ejemplo donde la ecualización no es útil (como vimos en teoria).
"""

PATH = '../images/'

img = cv2.imread(PATH + "coins.tif", cv2.IMREAD_GRAYSCALE)
img_eq = cv2.equalizeHist(img)  # imagen ecualizada
hist = cv2.calcHist([img],[0],None,[256],[0,256])
hist_eq = cv2.calcHist([img_eq],[0],None,[256],[0,256])

fig, axs = plt.subplots(2, 2)

axs[0,0].imshow(img, cmap='gray')
axs[0,0].set_title('Imagen original')

axs[1,0].imshow(img_eq, cmap='gray')
axs[1,0].set_title('Imagen ecualizada')

axs[0,1].plot(hist)
axs[0,1].set_title('Histograma original')

axs[1,1].plot(hist_eq)
axs[1,1].set_title('Histograma ecualizado')

plt.show()