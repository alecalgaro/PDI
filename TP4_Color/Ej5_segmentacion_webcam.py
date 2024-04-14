import argparse
import segment_color_rgb_webcam as scw_rgb
import segment_color_hsv_webcam as scw_hsv

# Si lo quiero usar desde consola:
# python Ej5_segmentacion_webcam.py -m "modeloDeColor"
# python Ej5_segmentacion_webcam.py -m "rgb"

DEFAULT_MODEL_COLOR = "rgb"

ap = argparse.ArgumentParser() 
ap.add_argument("-m", "--model", required=False, help="modelo de color a utilizar (rgb o hsv)")
args = vars(ap.parse_args())

model_color = args["model"] if args["model"] else DEFAULT_MODEL_COLOR

if(model_color == "rgb"):   #* Segmentacion de color en webcam utilizando modelo de color RGB.
    scw_rgb.segment_color_rgb_webcam()
else:   #* Segmentacion de color en webcam utilizando modelo de color HSV.
    scw_hsv.segment_color_hsv_webcam()