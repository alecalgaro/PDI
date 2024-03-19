import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2

# Este es un ejemplo acerca de la utilizacion de eventos del mouse para dibujar una
# linea, en este caso se utiliza el boton izquierdo al presionar y al soltar.

imagen = cv2.imread("futbol.jpg")
cv2.imshow("Imagen", imagen)

# Inicializa refPt como una lista vacia para guardar las posiciones donde se presiona y suelta el boton del mouse
refPt = []

# Se define la funcion que captura los clicks del mouse.
# Es la funcion que se llamara cuando ocurra un evento de mouse (callbackFunction). 
# Esta funcion debe tener un formato especifico, aceptando argumentos para el evento de mouse, 
# las coordenadas x e y del evento, cualquier bandera asociada con el evento y cualquier parametro adicional.
def click(event, x, y, flags, param):
    """
    Recordar el uso de "global" para indicar que la variable es global, es decir, puede ser 
    accedida y modificada desde cualquier parte del codigo. En este caso, si no se usa global 
    la variable refPt se crearia como local cada vez que se llama a la funcion y se perderia 
    la informacion de la posicion del mouse que ya tenia almacenada. 
    """
    global refPt    
    # si se presiona el boton izquierdo, se guarda la localizacion (x,y)
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        # con eso inicializa la lista refPt con esa posicion del mouse, pero si yo haria
        # refPt.append((x, y)) eso iria agregando posiciones a la lista y seria necesario limpiar
        # la lista cada vez que se quiera dibujar una linea nueva, es decir, luego de haberla 
        # dibujado, se deberia hacer refPt = [] para limpiar la lista 

    # si se suelta el boton, se guarda la localizacion (x,y)
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        # dibuja la linea entre los dos puntos y muestra la imagen
        # cv2.line(imagen, start_point, end_point, color, thickness, line_type)
        cv2.line(imagen, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow(str_win, imagen)

# defino una ventana y le asigno el manejador de eventos
str_win = "DibujaWin"
cv2.namedWindow(str_win)
cv2.setMouseCallback(str_win, click)
# setMouseCallback recibe el nombre de la ventana y la funcion que maneja los eventos del mouse, 
# ya que registra una devolucion de llamada (callback) cuando ocurra un evento de mouse en la ventana

#? Para cerrar la ventana se debe presionar la tecla "c"
while True:
    # muestra la ventana con la imagen y espera una tecla
    cv2.imshow(str_win, imagen)
    # espera a que se presione una tecla, el 0 indica que espera indefinidamente, pero el 1 indica que
    # espera 1 ms antes de pasar a la siguiente linea de codigo. Y el 0xFF es una operacion bit a bit
    # para obtener el valor ASCII de la tecla presionada.
    key = cv2.waitKey(1) & 0xFF
    # si la tecla c es presionada sale del while
    if key == ord("c"):
        # tambien podria usar cv2.destroyAllWindows() y luego break
        break