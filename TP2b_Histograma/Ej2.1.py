import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt
import cvui

#! FALTARIA PROBAR HACERLO CON UNA MASCARA Y USAR LA ECUALIZACION NORMAL, PARA QUE SEA LOCAL
#! PERO SIN USAR LA ADAPTATIVA.
 
"""
Enunciado:
En la imagen cuadros.tif se observa un conjunto de cuadros negros sobre un fondo casi uniforme. 
Utilice ecualizacion local del histograma para revelar los detalles ocultos en la imagen y compare 
los resultados con los obtenidos con ecualizacion global.

Ayuda: el tamaño de ventana y su localizacion es clave para realizar la ecualizacion local.
"""

"""
Aclaración:
De todo el codigo que hicimos, en realidad solo hace falta la parte de graficar los histogramas que
lo hice al final. El resto, que serian los trackbars para uso en tiempo real y el boton con cvui es
extra para dejarlo mejor y probar cosas.
"""

PATH = "../images/"

img = cv2.imread(PATH + "cuadros.tif", cv2.IMREAD_GRAYSCALE)

# plt.figure()
# plt.imshow(img, cmap="grey")
# plt.show()

"""
Para aclarar los cuadros negros en la imagen, en la ecualizacion local con la ecualización 
adaptativa del histograma (CLAHE) se fue ajustando el límite de recorte (clipLimit) y el tamaño 
de la cuadrícula (tileGridSize). Estos parámetros controlan el contraste de la imagen.

El clipLimit es un parámetro que limita el contraste de la imagen. Un valor más alto aumenta el contraste.
El tileGridSize es el tamaño de la cuadrícula para la ecualización local. Un tamaño de cuadrícula 
más pequeño da como resultado una ecualización más local y puede ayudar a resaltar los detalles 
en áreas más pequeñas.

Como en la imagen se puede ver que los cuadros negros son de aproximadamente 120 x 120, 
se fue probando con valores de tileGridSize menores, hasta obtener un resultado que, junto al 
clipLimit, permitieron reconocer el contenido que había oculto en los cuadros negros.

Se obtuvo un buen resultado (se puede reconocer claramente el contenido oculto) por ejemplo con:
clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(20,20))
"""

"""
Primero creamos un script que permite modificar los valores de clipLimit y tileGridSize con trackbars
y ver como afectan a la imagen ecualizada con CLAHE en tiempo real, para elegir la mejor combinacion
de valores.
"""

# Variables globales para guardar los valores de los trackbars y usarlos al final
clipLimit_global = 0
tileGridSize_global = 0

# Función para el trackbar (no hace nada, solo es necesario para cv2.createTrackbar)
# (Lo hice asi para recordar que tambien se puede usar trackbars de esta manera).
def nothing(x):
    pass

# Crea una ventana (usar el mismo nombre en los trackbars y cvui)
cv2.namedWindow('Controles')

# Crea una imagen para la interfaz de usuario
ui = np.zeros((250, 500), np.uint8)

# Inicializa cvui 
cvui.init('Controles')

# Valores iniciales para los trackbars
clipLimit = [10]
tileGridSize = [60]

# Bucle infinito para que se actualice en tiempo real la imagen con los valores de los trackbars
while(1):   
    ui[:] = (50)
    
    # El clipLimit lo hago variar de a 0.1 y el tileGridSize de a 1 porque debe ser entero
    cvui.text(ui, 50, 20, "ClipLimit")
    cvui.trackbar(ui, 50, 50, 400, clipLimit, 1, 100, 0.1, '%.0Lf', cvui.TRACKBAR_DISCRETE, 0.1)
    cvui.text(ui, 50, 100, "TileGridSize")
    cvui.trackbar(ui, 50, 130, 400, tileGridSize, 1, 100, 1, '%.0Lf', cvui.TRACKBAR_DISCRETE, 1)

    # Me aseguro que tileGridSize sea al menos 1
    if tileGridSize[0] == 0:
        tileGridSize[0] = 1

    # Aplica CLAHE con los valores actuales de los trackbars
    clahe = cv2.createCLAHE(clipLimit=float(clipLimit[0]), tileGridSize=(tileGridSize[0],tileGridSize[0]))
    cl1 = clahe.apply(img)

    # Muestra la imagen (se crea en una ventana distinta que la UI porque sino da problemas)
    cv2.imshow('Ecualizacion adaptativa', cl1)

    # Se dibuja el botón en la imagen de la interfaz de usuario
    if cvui.button(ui, 50, 200, "Usar estos valores"):
        # Al presionar el botón se guardan los valores de los trackbars para usarlos en el resto del codigo
        clipLimit_global = clipLimit[0]
        tileGridSize_global = tileGridSize[0]
        break

    # Muestra la interfaz de usuario
    cvui.imshow('Controles', ui)

    # Espera a que se presione la tecla ESC para salir
    if cv2.waitKey(20) == 27:
        # Al cerrar la ventana se guardan los valores de los trackbars para usarlos en el resto del codigo
        clipLimit_global = clipLimit[0]
        tileGridSize_global = tileGridSize[0]
        break

cv2.destroyAllWindows() # Cierro todas las ventanas cuando sale del bucle

"""
Una vez que se eligen los parametros con los trackbars y se cierra la ventana, se utilizan dichos valores para graficar los
histogramas y hacer la comparativa entre el histograma original, la ecualización tradicional
y la ecualización adaptativa.

Esta es la parte importante del codigo, el resto es solo para elegir los parametros con trackbars.
"""

# Histograma original
hist = cv2.calcHist([img],[0],None,[256],[0,256])  

# Ecualizacion global
img_eq = cv2.equalizeHist(img)  
hist_eq = cv2.calcHist([img_eq],[0],None,[256],[0,256]) # histograma ecualizado

# Ecualizacion adaptativa o local (CLAHE)
clahe = cv2.createCLAHE(clipLimit=clipLimit_global, tileGridSize=(tileGridSize_global,tileGridSize_global))
cl1 = clahe.apply(img)  # imagen ecualizada con CLAHE
hist_cl1 = cv2.calcHist([cl1],[0],None,[256],[0,256]) # histograma ecualizado con CLAHE

fig, axs = plt.subplots(2, 3)

axs[0,0].imshow(img, cmap='gray')
axs[0,0].set_title('Imagen original')

axs[1,0].plot(hist)
axs[1,0].set_title('Histograma original')

axs[0,1].imshow(img_eq, cmap='gray')
axs[0,1].set_title('Imagen ecualizada')

axs[1,1].plot(hist_eq)
axs[1,1].set_title('Histograma ecualizado')

axs[0,2].imshow(cl1, cmap='gray')
axs[0,2].set_title('Imagen ecualizada con CLAHE')

axs[1,2].plot(hist_cl1)
axs[1,2].set_title('Histograma ecualizado con CLAHE')

plt.show()