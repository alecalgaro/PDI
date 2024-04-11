import cv2
import numpy as np
import cvui
import utils as ut
import math


def get_sl_data(method, sp_params):
    """Definimos valores para dibujar una grafica usando cvui.sparkline.
    Para eso recibimos el metodo que queremos graficar.

    Parameters:
        method: TODO
    Returns:
        TODO

    """
    idt_fun = np.arange(0,255, 1)
    if method == "Logaritmica":
        return ut.computeLog(idt_fun, sp_params['c'])
    elif method == "Potencia":
        return ut.computePow(idt_fun, sp_params['g'], sp_params['c'])
    elif method == "LUT":
        # TODO: tratar de concatenar las salidas como hago en plotlut #
        lut_fun = np.array([])
        for i in range(len(sp_params["Rlims"])):
            if sp_params["Rlims"][i][0] != sp_params["Rlims"][i][1]:
                R = np.arange(sp_params["Rlims"][i][0],
                            sp_params["Rlims"][i][1]+1, 1)
                aux=ut.computeLUT(R, sp_params["A"][i], sp_params["C"][i])
                lut_fun=np.concatenate([lut_fun,aux])

        return lut_fun
    elif method=="Ninguna":
        return idt_fun

IMAGE_DIR = "../images/"
IMAGE_FILE = "earth.bmp"
imagen = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)
nimagen = imagen

WINDOW_NAME_1 = "Imagen"
WINDOW_NAME_2 = "Panel de control"
cv2.namedWindow(WINDOW_NAME_1)
cv2.namedWindow(WINDOW_NAME_2)
cvui.init(WINDOW_NAME_1)
cvui.watch(WINDOW_NAME_2)

frame = np.zeros((600, 540, 3), np.uint8)

Clog_val = [3.]
Cexp_val = [3.]
Gexp_val = [2.]
Xlut1_val = [50]
Xlut2_val = [150]
Ylut1_val = [50]
Ylut2_val = [150]
func_act = "Ninguna"
sp_params=[]
while (True):
    if cv2.waitKey(1) == ord("q"):
        break

    cvui.context(WINDOW_NAME_2)
    frame[:]=(49, 52, 49)

    cvui.text(frame, 10, 10, "Logaritmica")
    cvui.text(frame, 10, 40, "C: ", 0.5)
    if(cvui.trackbar(frame, 25, 30, 220, Clog_val, 0.1, 10.)):
        func_act = "Logaritmica"
        sp_params={'c':Clog_val[0]}

    cvui.text(frame, 10, 70, "Potencia")
    cvui.text(frame, 10, 100, "C: ", 0.5)
    if(cvui.trackbar(frame, 25, 90, 220, Cexp_val, 0.1, 10.)):
        func_act = "Potencia"
        sp_params={'c':Cexp_val[0], 'g':Gexp_val[0]}

    cvui.text(frame, 250, 100, "G: ", 0.5)
    if(cvui.trackbar(frame, 265, 90, 220, Gexp_val, 0.1, 10.)):
        func_act = "Potencia"
        sp_params={'c':Cexp_val[0], 'g':Gexp_val[0]}

    cvui.text(frame, 10, 150, "LUT por tramos")
    cvui.text(frame, 10, 180, "X1: ", 0.5)
    if(cvui.trackbar(frame, 30, 170, 220, Xlut1_val, 0, 255)):
        func_act = "LUT"
    cvui.text(frame, 270, 180, "Y1: ", 0.5)
    if(cvui.trackbar(frame, 300, 170, 220, Ylut1_val, 0, 255)):
        func_act = "LUT"
    cvui.text(frame, 10, 220, "X2: ", 0.5)
    if(cvui.trackbar(frame, 30, 230, 220, Xlut2_val, 0, 255)):
        func_act = "LUT"
    cvui.text(frame, 270, 220, "Y2: ", 0.5)
    if(cvui.trackbar(frame, 300, 230, 220, Ylut2_val, 0, 255)):
        func_act = "LUT"

    if func_act == "LUT":
        y1, y2 = Ylut1_val[0], Ylut2_val[0]
        if Xlut1_val[0] < Xlut2_val[0]:
            x1, x2 = Xlut1_val[0], Xlut2_val[0]
        else:
            x1, x2 = Xlut2_val[0], Xlut1_val[0]
        A, C, Rlims = ut.hacerTramos([(x1,y1),(x2,y2)])
        sp_params = {"A":A, "C":C, "Rlims":Rlims}

    sp_pts=get_sl_data(func_act, sp_params)
    cvui.sparkline(frame, sp_pts, 100, 320, 255, 255, 0xff0000);

    cvui.text(frame, 320, 20, f"Usando: {func_act}", 0.7)

    cvui.update(WINDOW_NAME_2)
    cvui.imshow(WINDOW_NAME_2, frame)

    cvui.context(WINDOW_NAME_1)
    if func_act == "Logaritmica":
        nimagen=ut.computeLog(imagen, Clog_val[0])
    elif func_act == "Potencia":
        nimagen=ut.computePow(imagen, Gexp_val[0], Cexp_val[0])
    elif func_act == "LUT":
        nimagen = ut.applyLUT(imagen, A, C, Rlims)

    cvui.update(WINDOW_NAME_1)
    cvui.imshow(WINDOW_NAME_1, nimagen)

