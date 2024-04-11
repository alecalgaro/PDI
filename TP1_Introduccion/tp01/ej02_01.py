import cv2


def click_cb(event, x, y, flags, param):
    global refPt, imagen
    # si se presiona el botón izquierdo, se guarda la localización (x,y)
    if event == cv2.EVENT_LBUTTONUP:
        refPt = (x, y)
        print(f"Point ({x}, {y}): {imagen[y,x]}")


IMAGE_DIR = "../images/"
IMAGE_FILE = "futbol.jpg"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}")
refPt = []

str_win="Colors by clicking"
cv2.namedWindow(str_win)
cv2.setMouseCallback(str_win, click_cb)

while True:
    # muestra la imagen y espera una tecla
    cv2.imshow(str_win, imagen)
    key = cv2.waitKey(1) & 0xFF
    # si la tecla x es presionada sale del while
    if key == ord("x"):
        break
