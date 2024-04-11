import cv2
import numpy as np
import cvui
import utils as ut

# TODO: Probar agregar ruido personalmente #
def pred_type(mse, ref, oth, TH=150.):
    """TODO: Docstring for pred_type.

    Parameters:
        mse: TODO
        ref: TODO
        oth: TODO
        TH: TODO
    Returns:
        TODO

    """
    if mse < TH:
        return ref
    else:
        return oth


def importGIF(path):
    """Funcion para importar una imagen en GIF.

    Parameters:
        path: Localizacion de la imagen
    Returns:
        imagen: Imagen cargada

    """
    vidcap = cv2.VideoCapture(path)
    _, imagen = vidcap.read()
    vidcap.release()
    return imagen

IMAGE_DIR = "../images/"
IMAGE_FILE_1 = "a7v600-X.gif"
IMAGE_FILE_2 = "a7v600-SE.gif"
IMAGE_FILE_3 = "a7v600-X(RImpulsivo).gif"
IMAGE_FILE_4 = "a7v600-SE(RImpulsivo).gif"

imagen1 = importGIF(f"{IMAGE_DIR}{IMAGE_FILE_1}")
imagen1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
imagen2 = importGIF(f"{IMAGE_DIR}{IMAGE_FILE_2}")
imagen2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2GRAY)
imagen3 = importGIF(f"{IMAGE_DIR}{IMAGE_FILE_3}")
imagen3 = cv2.cvtColor(imagen3, cv2.COLOR_BGR2GRAY)
imagen4 = importGIF(f"{IMAGE_DIR}{IMAGE_FILE_4}")
imagen4 = cv2.cvtColor(imagen4, cv2.COLOR_BGR2GRAY)

mascara = ut.computeLog(ut.diferencia(imagen2, imagen1, "no"), c=9.5)
grnd_tr = ut.multiplicacion(imagen2, mascara)
REFERENCE = "a7v600-SE"
OTHER = "a7v600-X"
img1mas = ut.multiplicacion(imagen1, mascara)
img2mas = ut.multiplicacion(imagen2, mascara)
img3mas = ut.multiplicacion(imagen3, mascara)
img4mas = ut.multiplicacion(imagen4, mascara)

WINDOW_NAME_1 = "Mascara"
WINDOW_NAME_2 = "Referencia (Placa SE)"
WINDOW_NAME_3 = "Placa X enmascarada"
WINDOW_NAME_4 = "Placa SE enmascarada"
WINDOW_NAME_5 = "Placa ruidosa X enmascarada"
WINDOW_NAME_6 = "Placa ruidosa SE enmascarada"

cv2.namedWindow(WINDOW_NAME_1)
cv2.namedWindow(WINDOW_NAME_2)
cv2.namedWindow(WINDOW_NAME_3)
cv2.namedWindow(WINDOW_NAME_4)
cv2.namedWindow(WINDOW_NAME_5)
cv2.namedWindow(WINDOW_NAME_6)

cvui.init(WINDOW_NAME_1)
cvui.watch(WINDOW_NAME_2)
cvui.watch(WINDOW_NAME_3)
cvui.watch(WINDOW_NAME_4)
cvui.watch(WINDOW_NAME_5)
cvui.watch(WINDOW_NAME_6)

while (True):
    if cv2.waitKey(1) == ord("q"):
        break

    cvui.imshow(WINDOW_NAME_1, mascara)
    cvui.update(WINDOW_NAME_1)

    cvui.imshow(WINDOW_NAME_2, grnd_tr)
    cvui.update(WINDOW_NAME_2)

    frame1 = np.copy(img1mas)
    mse1 = ut.mse(grnd_tr, img1mas)
    type1 = pred_type(mse1, REFERENCE, OTHER)
    cvui.text(frame1, 10, 300, f"MSE={mse1:6.2f}, Type={type1}")
    cvui.imshow(WINDOW_NAME_3, frame1)
    cvui.update(WINDOW_NAME_3)

    frame2 = np.copy(img2mas)
    mse2 = ut.mse(grnd_tr, img2mas)
    type2 = pred_type(mse2, REFERENCE, OTHER)
    cvui.text(frame2, 10, 300, f"MSE={mse2:6.2f}, Type={type2}")
    cvui.imshow(WINDOW_NAME_4, frame2)
    cvui.update(WINDOW_NAME_4)

    frame3 = np.copy(img3mas)
    mse3 = ut.mse(grnd_tr, img3mas)
    type3 = pred_type(mse3, REFERENCE, OTHER)
    cvui.text(frame3, 10, 300, f"MSE={mse3:6.2f}, Type={type3}")
    cvui.imshow(WINDOW_NAME_5, frame3)
    cvui.update(WINDOW_NAME_5)

    frame4 = np.copy(img4mas)
    mse4 = ut.mse(grnd_tr, img4mas)
    type4 = pred_type(mse4, REFERENCE, OTHER)
    cvui.text(frame4, 10, 300, f"MSE={mse4:6.2f}, Type={type4}")
    cvui.imshow(WINDOW_NAME_6, frame4)
    cvui.update(WINDOW_NAME_6)

