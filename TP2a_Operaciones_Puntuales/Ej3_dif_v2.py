import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui

PATH = "../images/"

"""
apply_Dif() calcula la diferencia entre dos imagenes o dos frames de un video, tomamos de la lista
de imagenes o frames "V_pics" y usando la funcion cv2.subtract.

La funcion cv2.subtract toma dos imagenes del mismo tamaño y devuelve la diferencia. 
La diferencia se calcula como la resta de los valores de los pixeles de una imagen con los de la otra.
Luego se convierte la imagen resultante a escala de grises y se aplica un umbral (con threshold)  
para obtener una imagen binaria. 
ret es el valor del umbral que se uso y mask es la imagen binaria.

mask != 255 devuelve una matriz de booleanos que es True en los pixeles que no son blancos.
Entonces lo que se hace es que en la imagen F, se pone en blanco (255,255,255) los pixeles que 
no eran blancos en la mascara (eran negros en la mascara o imagen binaria). Eso tiene el efecto de
"blanquear" las areas de F que son consideradas "primer plano" por la mascara.

Si no se usan las lineas de threshold y F[mask != 255] sirve igual, pero eso da un mejor resultado.

cv2.subtract realiza la misma operacion de resta que el operador "-", pero "satura" el resultado en
lugar de permitir que haya desbordamiento (que se pase de 255 y vuelva a comenzar en 0 y al revés).
Eso significa que si el resultado de la resta es menor a 0, cv2.subtract coloca 0, y si el resultado
es mayor a un valor máximo (255), cv2.subtract coloca ese valor máximo. 
Entonces la diferencia entre cv2.subtract y el operador "-" es que "-" permite el desbordamiento  
(hay que evitarlo desde el codigo) y cv2.subtract satura los resultados para evitarlo.
"""

def apply_Dif():
    global V_pics,F, N
    
    # N[0] es la cantidad de imagenes elegidas con el trackbar
    F = cv2.subtract(V_pics[N[0]-1], V_pics[N[0]])
    
    Conv_hsv_Gray = cv2.cvtColor(F, cv2.COLOR_BGR2GRAY) 
    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
    F[mask != 255] = [255, 255, 255]
    return F 
    
#----------------------------------------------------------------------------#

w_title1 = 'Panel de control'
w_title2 = 'Imagen Resultante'

V_pics = []
F = []

# Cargo el video
cap = cv2.VideoCapture(PATH + "pedestrians.mp4")
# Ciclo while para leer cada frame y guardarlo en la lista de imagenes
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #V_pics.append(gray)
        V_pics.append(frame.copy())  # voy almacenando los frames en la lista de imagenes
    else:   # Si no hay mas frames (ret = False), corto el ciclo
        break
cap.release()   # libero el video

F = V_pics[0].copy()    # Inicializo F con la primer imagen

# Inicializo la interfaz y creo una nueva ventana
cvui.init(w_title1, 20)
cv2.namedWindow(w_title2)

# Creo una imagen de 290x350 con 3 canales de color y llena de ceros (imagen negra) 
frame = np.zeros((200, 350, 3), np.uint8)

N = [1]

#Trackbar variables 
# (ancho de la ventana de trackbar y posicion en x para usar en el trackbar, boton y texto)
TB_width = 300
TB_x = 20

# Buble principal. 
while True:
    # Color del fondo de la pantalla del cvui
    frame[:] = (50, 50, 50)
    
    # Texto en la ventana
    cvui.text(frame, TB_x, 20, 'Cantidad de imagenes a combinar:')

    # Trackbar de cvui para seleccionar la cantidad de imagenes a combinar
    needs_calc = cvui.trackbar(frame, TB_x, 50, TB_width, N, 1, int(len(V_pics)-1), 2, '%.0Lf', cvui.TRACKBAR_DISCRETE, 1)
    
    # Boton para salir
    if cvui.button(frame, TB_x, 150, '&Cerrar'):
        cv2.destroyAllWindows()
        break
    
    # Actualizo la interfaz
    cvui.update()
    
    # Si se cambió la cantidad de imagenes a combinar (se cambia el trackbar -> needs_calc = True), 
    # recalculo la imagen resultante F con la nueva cantidad de imagenes
    if needs_calc:
        F = apply_Dif()
    
    # Muestro las imagenes en las ventanas
    cvui.imshow(w_title1, frame)
    cv2.imshow(w_title2, F)

    # Si se presiona la tecla 'ESC', cierro la ventana
    if cv2.waitKey(20) == 27:
        cv2.destroyAllWindows()
        break