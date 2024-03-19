import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2

# como usa valores naturales, ajusto la cantidad de valores a elegir
alpha_slider_max = 100
title_window = 'Titulo ventana'
imagen1 = cv2.imread("futbol.jpg")
imagen2 = cv2.imread("sillas.jpg")

# Redimensiona imagen2 para que tenga las mismas dimensiones que imagen1, porque 
# addWeighted requiere que las imagenes tengan las mismas dimensiones
imagen2 = cv2.resize(imagen2, (imagen1.shape[1], imagen1.shape[0]))

# se utilizan las 2 imagenes y se calculan los parametros para combinarlas.
# La funcion on_trackbar_alpha debe recibir un solo argumento, que es el valor del trackbar,
# ya que en cv2.createTrackbar se necesita pasar una funcion asi, por lo que se definen las 
# variables alpha y beta dentro de la funcion on_trackbar_alpha
def on_trackbar_alpha(val):
    global imagen1, imagen2, dst
    alpha = val / alpha_slider_max
    beta = ( 1.0 - alpha )
    dst = cv2.addWeighted(imagen1, alpha, imagen2, beta, 0.0)   
    # addWeighted combina las imagenes de entrada con los pesos alpha y beta
    # dst = alpha*imagen1 + beta*imagen2 + gamma
    # Las dos imagenes que se quieren combinar deben tener las mismas dimensiones
    # cv2.imshow(title_window, dst)

# se crea la ventana y el trackbar
# cv2.imshow(title_window, dst) # esta linea aca no funciona, porque dst no esta definido dice,
# entonces la agregue arriba pero tampoco es necesaria porque ya esta en el while           
cv2.namedWindow(title_window)

# Parametros de cv2.createTrackbar:
# 'Nombre del trackbar'
# 'Nombre de la ventana'
# Valor inicial del tackbar 
# Valor maximo permitido (ira desde 0 hasta ese valor)
# Funcion de callback que se ejecuta cada vez que cambie el valor del trackbar. Esta función 
# automaticamente toma un solo argumento que es el nuevo valor del trackbar.
cv2.createTrackbar('Alpha', title_window, int(alpha_slider_max/2), alpha_slider_max,
on_trackbar_alpha)

while True:
    cv2.imshow(title_window, dst) # se muestra la imagen combinada y el trackbar
    key = cv2.waitKey(1) & 0xFF
    # presione c para salir
    if key == ord("c"):
        break