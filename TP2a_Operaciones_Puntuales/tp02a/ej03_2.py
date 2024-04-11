import cv2
import numpy as np
from matplotlib import pyplot as plt
import cvui
import utils as ut

IMAGE_DIR = "../images/"
VIDEO_FILE = "pedestrians.mp4"
cap = cv2.VideoCapture(f"{IMAGE_DIR}{VIDEO_FILE}")
frames=[]
print("Cargando video...")
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))


frames=np.array(frames)
cant_frm = [1]
c=cant_frm[0]
prom = ut.suma_promedio(frames[:c])

WINDOW_NAME = "Video background"
cvui.init(WINDOW_NAME)
while(True):

    cvui.imshow(WINDOW_NAME, prom)
    if(cvui.trackbar(prom, 10, prom.shape[0]-50, 200, cant_frm, int(1),
                     int(len(frames)))):
        c=int(cant_frm[0])
        prom = ut.suma_promedio(frames[:c])
    cvui.text(prom, 220, prom.shape[0]-30, f"Frames promediados: {c}", 0.4,
              0x000000)

    cvui.update()

    if cv2.waitKey(1) == ord("q"):
        break
