import cv2

#? 7. Dibuje sobre la imagen lineas, circulos y rectangulos (opcional: defina la posicion en base al click del mouse).

image = cv2.imread('1. Introduccion/images/cameraman.tif')

#? Primero dibujo en la imagen en posiciones fijas, sin usar el mouse.

cv2.line(image, (0, 0), (100, 100), (255, 0, 0), 5)
cv2.circle(image, (100, 100), 50, (0, 255, 0), 3)
cv2.rectangle(image, (200, 200), (300, 300), (0, 0, 255), 2)

cv2.imshow('Imagen con figuras', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#? Ahora dibujo en base al click del mouse.

image = cv2.imread('1. Introduccion/images/flores.jpg')

# Para linea uso la misma funcion que cree en el ejercicio 6 de la guia de introduccion a OpenCV,
# para dibujar entre dos puntos al presionar y soltar el mouse
refPt = []
def draw_line(event, x, y, flags, param):
    global refPt    
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        # dibuja la linea entre los puntos
        cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 2)
      
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, (x, y), 50, (0, 255, 0), 3)   
        # cv2.imshow('Imagen con circulo', image)   # la muestro en el while 

def draw_rectangle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(image, (x, y), (x+100, y+100), (0, 0, 255), 2)

#* Se define una ventana y se le asigna el manejador de eventos.
#* Hay que descomentar la linea correspondiente a linea, circulo o rectangulo, segun lo que se quiera.
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen', draw_line)   # parametros: nombre de la ventana que se usa y funcion que maneja los eventos del mouse
# cv2.setMouseCallback('Imagen', draw_circle)
# cv2.setMouseCallback('Imagen', draw_rectangle)

while True:
    # muestra la ventana con la imagen y espera una tecla
    cv2.imshow("Imagen", image)
    key = cv2.waitKey(1) & 0xFF
    # si la tecla c es presionada sale del while
    if key == ord("c"):
        break
