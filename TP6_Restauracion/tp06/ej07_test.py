import cv2
import numpy as np
import utils.ruidos as ns
import matplotlib.pyplot as plt
import cvui

PADX, PADY = 10, 10

IMAGE_DIR = "../images/"
#IMAGE_FILE = "FAMILIA_a.jpg"
#IMAGE_FILE = "FAMILIA_b.jpg"
IMAGE_FILE = "FAMILIA_c.jpg"
noised = cv2.imread(f"{IMAGE_DIR}{IMAGE_FILE}", cv2.IMREAD_GRAYSCALE)
# TODO: Usar como noised una roi y el histograma #
noised = noised[:500,:700]
ISHY, ISHX = noised.shape

frame = np.zeros((450, 900, 3), np.uint8)

###############################################################################
#                       Variables del panel de control                        #
###############################################################################
tipo_str="MEDIA GEOMETRICA"
geo_M  = [3]
cth_M  = [3]
cth_Q  = [0]
med_M  = [3]
mid_M  = [3]
atm_M  = [3]
atm_D  = [2]
alm_M  = [3]
alm_V  = [5]
dbil = [3]
sbilC = [1.]
sbilS = [1.]

WINDOW_NAME_1 = "Imagen con ruido"
cv2.namedWindow(WINDOW_NAME_1)
cvui.init(WINDOW_NAME_1)
WINDOW_NAME_2 = "Panel de control del filtro"
cv2.namedWindow(WINDOW_NAME_2)
cvui.watch(WINDOW_NAME_2)
WINDOW_NAME_3 = "Imagen filtrada"
cv2.namedWindow(WINDOW_NAME_3)
cvui.watch(WINDOW_NAME_3)

filtrar = True
while (True):
    if cv2.waitKey(1) == ord("q"):
        break

    ##########################################################################
    #                            Imagen con ruido                            #
    ##########################################################################
    cvui.context(WINDOW_NAME_1)
    cvui.update(WINDOW_NAME_1)
    cv2.imshow(WINDOW_NAME_1, noised)

    ##########################################################################
    #                            Panel de control                            #
    ##########################################################################
    cvui.context(WINDOW_NAME_2)
    frame[:]=(49, 52, 49)
    cvui.text(frame, PADX, PADY, f"Tipo actual: {tipo_str}", 0.5)
    cvui.text(frame, PADX, 5*PADY, f"M (m. geom.): ")
    if(cvui.trackbar(frame, 15*PADX, 3*PADY, 250, geo_M, 1, 20, 1, "%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "MEDIA GEOMETRICA"
    cvui.text(frame, PADX, 10*PADY, f"M (m. c. arm): ")
    if(cvui.trackbar(frame, 15*PADX, 8*PADY, 250, cth_M, 1, 20, 1, "%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "MEDIA CONTRA-ARMONICA"
    cvui.text(frame, PADX, 15*PADY, f"Q (m. c. arm.): ")
    if(cvui.trackbar(frame, 15*PADX, 13*PADY, 250, cth_Q, -10,10, 1, "%.2Lf")):
        filtrar = True
        tipo_str = "MEDIA CONTRA-ARMONICA"
    cvui.text(frame, 450+PADX, 5*PADY, f"M (mediana): ")
    if(cvui.trackbar(frame,450+15*PADX,3*PADY,250, med_M, 1, 20, 1, "%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "MEDIANA"
    cvui.text(frame, 450+PADX, 10*PADY, f"M (pto. medio): ")
    if(cvui.trackbar(frame,450+15*PADX,8*PADY,250,mid_M,1,20,1,"%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "PUNTO MEDIO"
    cvui.text(frame, 450+PADX, 15*PADY, f"M (med. alfa rec.): ")
    if(cvui.trackbar(frame,450+15*PADX,13*PADY,250,atm_M,1,20,1,"%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "ALFA MEDIA RECORTADO"
    cvui.text(frame, 450+PADX, 20*PADY, f"D (med. alfa rec.): ")
    if(cvui.trackbar(frame,450+15*PADX,18*PADY,250,atm_D,1,9,1,"%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "ALFA MEDIA RECORTADO"
    cvui.text(frame, PADX, 25*PADY, f"M (f. adapt.): ")
    if(cvui.trackbar(frame, 15*PADX, 23*PADY, 250, alm_M, 1, 20, 1, "%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "ADAPTATIVO LOCAL"
    cvui.text(frame, 450+PADX, 25*PADY, f"Vn (f. adapt.): ")
    if(cvui.trackbar(frame, 450+15*PADX, 23*PADY, 250, alm_V, 1, 500, 1, "%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "ADAPTATIVO LOCAL"
    cvui.text(frame, PADX, 30*PADY, f"D para Bilateral: ")
    if(cvui.trackbar(frame, 15*PADX, 28*PADY, 150, dbil, 1, 11, 1, "%.0Lf",
                     cvui.TRACKBAR_DISCRETE, 1)):
        filtrar = True
        tipo_str = "BILATERAL"
    cvui.text(frame, PADX, 35*PADY, f"SigmaC para Bilateral: ")
    if(cvui.trackbar(frame, 15*PADX, 33*PADY, 175, sbilC, 0, 250, 1,
                     "%.2Lf")):
        filtrar = True
        tipo_str = "BILATERAL"
    cvui.text(frame, 450+PADX, 35*PADY, f"SigmaS para Bilateral: ")
    if(cvui.trackbar(frame, 450+15*PADX, 33*PADY, 175, sbilS, 0, 250, 1,
                     "%.2Lf")):
        filtrar = True
        tipo_str = "BILATERAL"

    cvui.update(WINDOW_NAME_2)
    cvui.imshow(WINDOW_NAME_2, frame)

    ##########################################################################
    #                            Imagen filtrada                             #
    ##########################################################################
    cvui.context(WINDOW_NAME_3)
    if filtrar==True:
        filtrar=False
        if tipo_str == "MEDIA GEOMETRICA":
            filtered=ns.geometric_mean_filter(noised, geo_M[0])
        elif tipo_str == "MEDIA CONTRA-ARMONICA":
            filtered=ns.contraharmonic_mean_filter(noised, cth_M[0], cth_Q[0])
        elif tipo_str == "MEDIANA":
            filtered=ns.median_filter(noised, med_M[0])
        elif tipo_str == "PUNTO MEDIO":
            filtered=ns.midpoint_filter(noised, mid_M[0])
        elif tipo_str == "ALFA MEDIA RECORTADO":
            filtered = ns.alpha_trimmed_mean_filter(noised,atm_M[0],atm_D[0])
        elif tipo_str == "BILATERAL":
            filtered = cv2.bilateralFilter(noised, dbil[0], sbilC[0], sbilS[0])
        else:
            filtered = ns.adaptative_local_filter(noised, alm_M[0], alm_V[0])
    cvui.update(WINDOW_NAME_3)
    cv2.imshow(WINDOW_NAME_3, filtered)

