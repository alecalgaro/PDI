import cv2
from math import sqrt


def click_cb(event, x, y, flags, param):
    global refPt, imagen, drawing_line, drawing_circ, drawing_rect
    # si se presiona el botón izquierdo, se guarda la localización (x,y)
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        # si se libera el botón, se guarda la localización (x,y)
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        if drawing_line:
            cv2.line(imagen, refPt[0], refPt[1], (0, 255, 0), 2)
            drawing_line = False
        if drawing_circ:
            r=sqrt((refPt[0][0]-refPt[1][0])**2+(refPt[0][1]-refPt[1][1])**2)
            cv2.circle(imagen, refPt[0], int(r), (255, 0, 0), 2)
            drawing_circ = False
        if drawing_rect:
            cv2.rectangle(imagen, refPt[0], refPt[1], (0, 0, 255), 2)
            drawing_rect = False
        cv2.imshow(str_win, imagen)


IMAGE_DIR = "../images/"
IMAGE_FILE = "futbol.jpg"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}")
refPt = []

str_win="DibujaWin"
cv2.namedWindow(str_win)
cv2.setMouseCallback(str_win, click_cb)

drawing_line = False
drawing_circ = False
drawing_rect = False

while True:
    # muestra la imagen y espera una tecla
    cv2.imshow(str_win, imagen)
    key = cv2.waitKey(1) & 0xFF
    # si la tecla l es presionada dibuja una linea
    if key == ord("l"):
        drawing_line = True
        drawing_circ = False
        drawing_rect = False
    # si la tecla r es presionada dibuja un rectangulo
    if key == ord("r"):
        drawing_line = False
        drawing_circ = False
        drawing_rect = True
    # si la tecla c es presionada dibuja un circulo
    if key == ord("c"):
        drawing_line = False
        drawing_circ = True
        drawing_rect = False
    # si la tecla x es presionada sale del while
    if key == ord("x"):
        break
