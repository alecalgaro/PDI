"""
Funcion para calcular el histograma por canal de color de una imagen, 
en los espacios de color RGB y HSV.
"""

import cv2
import matplotlib.pyplot as plt

def hist_channel(img):
    # Calcular histograma por canal en el modelo de color RGB
    b, g, r = cv2.split(img)
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
    hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])

    # Calcular histograma por canal en el modelo de color HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    hist_h = cv2.calcHist([h], [0], None, [256], [0, 256])
    hist_s = cv2.calcHist([s], [0], None, [256], [0, 256])
    hist_v = cv2.calcHist([v], [0], None, [256], [0, 256])

    # Graficar los histogramas
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    axs[0, 0].plot(hist_r, color='red')
    axs[0, 0].set_title('Histograma de R (RGB)')
    axs[0, 1].plot(hist_g, color='green')
    axs[0, 1].set_title('Histograma de G (RGB)')
    axs[0, 2].plot(hist_b, color='blue')
    axs[0, 2].set_title('Histograma de B (RGB)')
    axs[1, 0].plot(hist_h, color='red')
    axs[1, 0].set_title('Histograma de H (HSV)')
    axs[1, 1].plot(hist_s, color='green')
    axs[1, 1].set_title('Histograma de S (HSV)')
    axs[1, 2].plot(hist_v, color='blue')
    axs[1, 2].set_title('Histograma de V (HSV)')
    plt.show()

    return hist_r, hist_g, hist_b, hist_h, hist_s, hist_v
