import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import argparse
import segment_color_rgb_video as scv_rgb
import segment_color_hsv_video as scv_hsv

# Si lo quiero usar desde consola:
# python Ej5_segmentacion_video.py -vi "nombreVideo.mp4" -m "modeloDeColor"
# python Ej5_segmentacion_video.py -vi "pedestrians.mp4" -m "rgb"

PATH = '../images/'

DEFAULT_VIDEO = "pedestrians.mp4"
DEFAULT_MODEL_COLOR = "rgb"

ap = argparse.ArgumentParser() 
ap.add_argument("-vi", "--video", required=False, help="path del video a utilizar")
ap.add_argument("-m", "--model", required=False, help="modelo de color a utilizar (rgb o hsv)")
args = vars(ap.parse_args())

nombre_video = args["video"] if args["video"] else DEFAULT_VIDEO
model_color = args["model"] if args["model"] else DEFAULT_MODEL_COLOR

# Leer el video
video = cv2.VideoCapture(PATH + nombre_video)

if(model_color == "rgb"):   #* Segmentacion de color en video utilizando modelo de color RGB.
    scv_rgb.segment_color_rgv_video(video)
else:   #* Segmentacion de color en video utilizando modelo de color HSV.
    scv_hsv.segment_color_hsv_video(video)