import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui

"""
A partir de un video (pedestrians.mp4) de una camara de seguridad, debe
obtener solamente el fondo de la imagen. Incorpore un elemento TrackBar
que le permita ir eligiendo el numero de frames a promediar para observar
los resultados instantaneamente.
"""

def promedio(images):
    """
    Funcion que calcula el promedio entre varias imagenes recibidas en un vector.
    """
    # Asegurarse de que todas las imágenes tienen el mismo tamaño
    for img in images[1:]:
        assert img.shape == images[0].shape, "Todas las imágenes deben tener el mismo tamaño"

    # Convertir las imágenes a float32 para evitar desbordamiento que puede ocurrir con uint8
    images = [img.astype(np.float32) for img in images]

    # Sumar todas las imágenes
    suma = np.sum(images, axis=0)

    # Calcular el promedio
    prom = suma / len(images)

    # Limitar los valores al rango de 0 a 255
    prom = np.clip(prom, 0, 255)

    # Convertir la imagen resultante a uint8 para poder mostrarla
    prom = prom.astype(np.uint8)

    return prom

# ----------------------------------------------------------------------------

PATH = "../images/"

w_title1 = 'Panel de control'
w_title2 = 'Fondo obtenido'

V_frames = []
fondo = []

# Cargo el video
cap = cv2.VideoCapture(PATH + "pedestrians.mp4")

# Ciclo while para leer cada frame y guardarlo en la lista de imagenes
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret: # Si hay un frame, lo guardo en la lista de imagenes
        #frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #V_frames.append(frame_gray)
        V_frames.append(frame.copy())
    else:  # Si no hay mas frames (ret = False), corto el ciclo
        break
cap.release()   # libero el video

# Inicializo el fondo con el primer frame del video
fondo = V_frames[0]

# Inicializo la interfaz de usuario y creo una nueva ventana para la imagen
cvui.init(w_title1)
cv2.namedWindow(w_title2)

# Creo una imagen de 3000x350 con 3 canales de color y llena de ceros (imagen negra) para la interfaz grafica
UI = np.zeros((200, 350, 3), np.uint8)


#Trackbar variables 
# (ancho de la ventana de trackbar y posicion en x para usar en el trackbar, boton y texto)
TB_width = 300
TB_x = 20
N = [1]     # Cantidad de imagenes a combinar (trackbar)

# Buble principal de la interfaz de usuario. 
# En cada iteracion se actualiza la interfaz y se procesan los eventos de la misma.
# El buble se ejecuta hasta que se presiona la tecla 'ESC' o se cierra la ventana.
while True:
    # Limpiar la UI - Color del fondo de la pantalla del cvui trackbar (gris oscuro)
    UI[:] = (50, 50, 50)
    
    # Texto en la ventana
    cvui.text(UI, TB_x, 40, 'Cantidad de imagenes a combinar:')

    # Trackbar de cvui para seleccionar la cantidad de imagenes a combinar
    # Si se cambia el valor del trackbar, "recalculate" cambia a True y se debe recalcular la imagen resultante
    recalculate = cvui.trackbar(UI, TB_x, 80, TB_width, N, 1, int(len(V_frames)), 2, '%.0Lf', cvui.TRACKBAR_DISCRETE, 1)
    
    # Boton para salir
    if cvui.button(UI, TB_x, 160, '&Cerrar'):
        cv2.destroyAllWindows()    # si se presiona el boton, se cierran las ventanas
        break

    # Actualizo la interfaz
    cvui.update()
    
    # Si se cambió la cantidad de imagenes a combinar (se cambia el trackbar -> recalculate = True), 
    # recalculo la imagen resultante "fondo" con la nueva cantidad de imagenes
    if recalculate:
        fondo = promedio(V_frames[:N[0]])
    
    # Muestro la interfaz de usuario y la imagen en las ventanas
    cvui.imshow(w_title1, UI)
    cv2.imshow(w_title2, fondo)

    # Si se presiona la tecla 'ESC', cierro la ventana
    if cv2.waitKey(20) == 27:
        cv2.destroyAllWindows()
        break