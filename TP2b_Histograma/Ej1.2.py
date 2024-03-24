import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

import Statistics_functions as sf

"""
Viendo las imagenes de los histogramas, pensar:
¿Es clara u oscura?, ¿tiene buen contraste?, ¿el histograma me explica algo respecto de la 
ubicacion de los grises?, etc.

Comentarios al ver las imágenes de histogramas:

-histo1.tif: es una imagen con mayor cantidad de px oscuros pero que tiene px distribuidos en todo
el rango. Tiene buen contraste ya que la diferencia entre el valor max y min de gris es grande, 
teniendo px cercanos a 0 y cercanos a 250. 
El histograma me muestra que la mayor cantidad de px se encuentra en los valores bajos, es decir, 
en los px oscuros.

-histo2.tif: es una imagen oscura, no cuenta con px claros (desde 160 aprox en adelante), la mayoria
de los px se centran entre niveles de gris de 50 a 150.
Tiene un contraste bajo, ya que la diferencia entre el valor maximo y minimo de gris es baja.

-histo3.tif: es una imagen oscura, todos los px se centran entre niveles de gris de 0 a 50.
Tiene un contraste bajo.

-histo4.tif: es una imagen clara, la mayoria de los px se centran entre niveles de gris de 200 a 250,
y en un nivel de gris 90 aproximadamente existe una pico alto en el histograma asi que habra gran
cantidad de px de ese nivel de gris.
Tiene un contraste bajo.

-histo5.tif: es una imagen clara, con buen contraste y una distribución de grises bastante pareja 
en el rango de 60 aprox hasta  250.
"""

"""
Correspondencia histograma-imagen:
histo1 -> imagenC
histo2 -> imagenA
histo3 -> imagenE
histo4 -> imagenB
histo5 -> imagenD
"""

PATH = '../images/'

# Cargar imagenes
imagenA = cv2.imread(PATH + 'imagenA.tif')
imagenB = cv2.imread(PATH + 'imagenB.tif')
imagenC = cv2.imread(PATH + 'imagenC.tif')
imagenD = cv2.imread(PATH + 'imagenD.tif')
imagenE = cv2.imread(PATH + 'imagenE.tif')

# Calcular histogramas
hist_imagenA = cv2.calcHist([imagenA], [0], None, [256], [0, 256])
hist_imagenB = cv2.calcHist([imagenB], [0], None, [256], [0, 256])
hist_imagenC = cv2.calcHist([imagenC], [0], None, [256], [0, 256])
hist_imagenD = cv2.calcHist([imagenD], [0], None, [256], [0, 256])
hist_imagenE = cv2.calcHist([imagenE], [0], None, [256], [0, 256])

"""
Si se quiere ver los histogramas tal como se ven en las imagenes de la carpeta, 
se los debe mostrar con cv2.imshow() y no con plt.plot(), o usar bar() de plt como hice.

Con bar() se crea un grafico de barras, donde el eje x es el nivel de gris y el eje y es la cantidad
de px de ese nivel de gris.

range(256) es para que el eje x vaya de 0 a 255, que son los niveles de gris posibles en una imagen
de 8 bits en escala de grises.

np.squeeze() es para que el histograma sea un array de 1 dimension y no de 2 dimensiones. 
Esa funcion np.squeeze() elimina las dimensiones que tienen tamaño 1 en la matriz dada, entonces
se usa para asegurarse que el histograma sea un array de 1 dimension que es lo que espera bar().
Si el histograma ya es un array de 1 dimension, np.squeeze() no hace nada.
"""

# Graficar histogramas
fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagenA, cmap='gray')
axs[0].set_title('imagenA.tif')
axs[1].bar(range(256), np.squeeze(hist_imagenA))    
axs[1].set_title('Histograma')

fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagenB, cmap='gray')
axs[0].set_title('imagenB.tif')
axs[1].bar(range(256), np.squeeze(hist_imagenB)) 
axs[1].set_title('Histograma')

fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagenC, cmap='gray')
axs[0].set_title('imagenC.tif')
axs[1].bar(range(256), np.squeeze(hist_imagenC)) 
axs[1].set_title('Histograma')

fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagenD, cmap='gray')
axs[0].set_title('imagenD.tif')
axs[1].bar(range(256), np.squeeze(hist_imagenD)) 
axs[1].set_title('Histograma')

fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagenE, cmap='gray')
axs[0].set_title('imagenE.tif')
axs[1].bar(range(256), np.squeeze(hist_imagenE)) 
axs[1].set_title('Histograma')

# plt.show()    # Lo punto en la linea final para que aparezcan las propiedades estadisticas 
                # primero y luego las graficas para no tener que cerrar las graficas para ver las propiedades.

"""
Obtenga y analice la utilidad de las propiedades estadisticas en los histogramas: 
media, varianza, asimetria, energia y entropia.
"""

#* Propiedades estadisticas del histograma de la imagenA
print('Propiedades estadisticas de la imagenA.tif:')
print('Media:', sf.media(hist_imagenA))
print('Varianza:', sf.varianza(hist_imagenA))
print('Asimetria:', sf.asimetria(hist_imagenA))
print('Energia:', sf.energia(hist_imagenA))
print('Entropia:', sf.entropia(hist_imagenA))
print()

#* Propiedades estadisticas del histograma de la imagenB
print('Propiedades estadisticas de la imagenB.tif:')
print('Media:', sf.media(hist_imagenB))
print('Varianza:', sf.varianza(hist_imagenB))
print('Asimetria:', sf.asimetria(hist_imagenB))
print('Energia:', sf.energia(hist_imagenB))
print('Entropia:', sf.entropia(hist_imagenB))
print()

#* Propiedades estadisticas del histograma de la imagenC
print('Propiedades estadisticas de la imagenC.tif:')
print('Media:', sf.media(hist_imagenC))
print('Varianza:', sf.varianza(hist_imagenC))
print('Asimetria:', sf.asimetria(hist_imagenC))
print('Energia:', sf.energia(hist_imagenC))
print('Entropia:', sf.entropia(hist_imagenC))
print()

#* Propiedades estadisticas del histograma de la imagenD
print('Propiedades estadisticas de la imagenD.tif:')
print('Media:', sf.media(hist_imagenD))
print('Varianza:', sf.varianza(hist_imagenD))
print('Asimetria:', sf.asimetria(hist_imagenD))
print('Energia:', sf.energia(hist_imagenD))
print('Entropia:', sf.entropia(hist_imagenD))
print()

#* Propiedades estadisticas del histograma de la imagenE
print('Propiedades estadisticas de la imagenE.tif:')
print('Media:', sf.media(hist_imagenE))
print('Varianza:', sf.varianza(hist_imagenE))
print('Asimetria:', sf.asimetria(hist_imagenE))
print('Energia:', sf.energia(hist_imagenE))
print('Entropia:', sf.entropia(hist_imagenE))
print()

# Mostrar graficas
plt.show() 