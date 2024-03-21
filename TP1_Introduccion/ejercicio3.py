"""
    Ejercicio 3: Aplicacion
    Utilice las herramientas aprendidas en esta unidad para implementar un sistema
    que permita identificar una botella que no esta correctamente llena. Las imagenes
    que se proporcionaran son capturadas con una camara fija, en escala de grises y
    directamente de la linea de envasado. Para implementar el sistema debera bastarle
    una imagen de ejemplo "botella.tif" (que encontrara en el repositorio). 
    
    Adicionalmente, se espera que el sistema pueda:
        -identificar una botella no-llena en cualquier posicion de la imagen.
        -indicar la posicion de la botella en la imagen (podra ser con un recuadro,
        informando la posicion relativa entre botellasNoLlenas, la posicion absoluta en pixels, etc).
        -informar el porcentaje de llenado de la botella no-llena.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
from matplotlib import pyplot as plt

"""
Con los temas aprendidos en la unidad, se puede implementar un sistema que permita identificar
una botella que no esta correctamente llena utilizando el calculo de perfiles de intensidad.
"""

PATH_IMAGE = '../images/botellas.tif'

#? Cargar imagen
img_original = cv2.imread(PATH_IMAGE, cv2.IMREAD_GRAYSCALE)
# plt.figure()
# plt.imshow(img_original, cmap='gray')
# plt.title('Imagen original')

"""
-Identificar botellasNoLlenas no llenas:
Viendo la imagen graficada con matplotlib, se puede ver que el contenido en las botellasNoLlenas llenas
alcanza y=45 (fila) aproximadamente. Por lo que se puede tomar dicho valor de "y" como referencia 
para el análisis de las botellasNoLlenas no llenas.

Al graficar el perfil de intensidad de la fila 45 se puede notar claramente si una botella 
no esta correctamente llena, ya que el perfil de intensidad será constante en 250 aproximadamente.
"""

#? Quitar borde blanco a la derecha y abajo de la imagen para que no interfiera en el análisis
img = img_original[0:img_original.shape[0]-1, 0:img_original.shape[1]-1]    # quitar borde derecho
img = img[0:img.shape[0]-1, :]  # quitar borde inferior
plt.figure()
plt.imshow(img, cmap='gray')
plt.title('Imagen original sin bordes blancos')

#? Graficar perfil de intensidad de la fila 45
plt.figure()
plt.plot(img[45, :])
plt.title('Perfil de intensidad de la fila 45')
plt.xlabel('Columna')
plt.ylabel('Intensidad')

"""
-Indicar la posicion de la botella en la imagen:
Para indicar la posicion de la botella no llena se puede utilizar un recuadro que delimite
la botella no llena. Para ello guardamos la primer y ultima columna donde la intensidad es mayor 
a un umbral de intensidad y luego se dibuja un recuadro sobre esa botella no llena.
El codigo contempla que puedan aparecer mas de una botella no llena en la imagen.

El umbral se determina probando que valor da el mejor resultado.
"""

umbral = 240                # umbral de intensidad para detectar botellasNoLlenas no llenas
botellasNoLlenas = []       # guardar las columnas de inicio y fin de las botellas no llenas
dentroDeBotella = False     # bandera para saber si estamos dentro de una botella no llena

for i in range(img.shape[1]):   # recorrer todas las columnas de la imagen
    if img[45, i] > umbral and not dentroDeBotella:     
        dentroDeBotella = True
        columna_inicio = i
    elif img[45, i] <= umbral and dentroDeBotella:
        dentroDeBotella = False
        columna_fin = i
        botellasNoLlenas.append((columna_inicio, columna_fin))

# Al final del bucle, botellasNoLlenas contiene tuplas con las columnas de inicio y fin de las 
# botellas no llenas.
        
# Dibujar un recuadro sobre las botellas no llenas
# Se dibuja -3 y +3 para que el recuadro no quede justo en el borde de la botella
img_recuadro = img.copy()
img_recuadro = cv2.cvtColor(img_recuadro, cv2.COLOR_GRAY2RGB)   # convertir a RGB para poder dibujar recuadros de color (opcional)
for botella in botellasNoLlenas:
    cv2.rectangle(img_recuadro, (botella[0]-3, 45), (botella[1]+3, img_recuadro.shape[0]), [255,0,0], 2)

# plt.figure()
# plt.imshow(img_recuadro)
# plt.title('Detección de botellas no llenas')

"""
-Determinar el porcentaje de llenado de la botella no llena:
Para determinar el porcentaje de llenado de la botella no llena, sabiendo que la botella llena 
llega hasta y=45, se puede buscar la altura de llenado de la botella no llena y calcular el
porcentaje de llenado en base a la altura de llenado de una botella llena.
"""

# Recorrer botellasNoLlenas, desde y=45 hacia abajo (filas), y buscar la altura de llenado, que 
# seria cuando la intensidad de la columna pasa a ser menor al umbral (un color mas oscuro).
# Se usa la columna_inicio de antes (botella[0]) y se va bajando por esa columna hasta encontrar
# que la intensidad sea menor al umbral, y esa altura de llenado se guarda en un arreglo.

umbral = 235    # defini un poco mas bajo el umbral que el otro porque probando con varias imagenes da mejor resultado
altura_llenado = []     # se guarda la altura (fila) de llenado de las botellas no llenas
for botella in botellasNoLlenas:
    for i in range(45, img.shape[0]):   # desde la fila y=45 hacia el borde inferior de la imagen (recorro las filas)
        if img[i, botella[0]] <= umbral:    
            altura_llenado.append(i)
            break

# Calcular porcentaje de llenado de botellasNoLlenas no llenas, sabiendo que la fila y=45 es el 
# 100% de llenado. Tener en cuenta que el "y" en la imagen crece de arriba hacia abajo, por eso 
# hago una conversion.

porcentaje_llenado = []     # se guarda el porcentaje de llenado de las botellas no llenas
for i in range(len(botellasNoLlenas)):
    # Como el "y" de la imagen crece de arriba hacia abajo, se puede hacer la resta de la altura
    # de llenado a la altura total de la imagen y luego dividir por la altura de la imagen y 
    # multiplicar por 100 para obtener el porcentaje de llenado.
    porcentaje_llenado.append((img.shape[0]-altura_llenado[i])/(img.shape[0]-45)*100)

print('Porcentaje de llenado de botellasNoLlenas no llenas:', porcentaje_llenado)

#? Marcar la linea de llenado de cada botella no llena y colocar el porcentaje arriba
# Dibujar una linea recta entre columna_inicio y columna_fin sobre esa altura de llenado
img_linea = img_recuadro.copy()
for i in range(len(botellasNoLlenas)):
    cv2.line(img_linea, (botellasNoLlenas[i][0], altura_llenado[i]), (botellasNoLlenas[i][1], altura_llenado[i]), [0,255,0], 2)
    # Dibujar el porcentaje de llenado sobre la línea
    cv2.putText(img_linea, f'{porcentaje_llenado[i]:.2f}%', (botellasNoLlenas[i][0], altura_llenado[i] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, [0,255,0], 1)

plt.figure()
plt.imshow(img_linea)
plt.title('Detección de botellas no llenas')

#? Mostrar todas las graficas
plt.show()