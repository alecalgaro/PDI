"""
Reconstruccion morfologica.
"""

import cv2

def reconst_morpho(img, mask):
    # img --> to reconstruct
    # mask --> original image to use as mask
    # process: dilate -> [img && !mask] --> repeat until img == img+1
    show = True
    while True:
        k = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        img_n = cv2.morphologyEx(img, cv2.MORPH_DILATE, k, iterations = 2)
        img_n = cv2.bitwise_and(img_n, mask)
        if (img_n == img).all():
            if show:
                cv2.imshow('Iterando...',img_n)
                cv2.waitKey(50)
            cv2.destroyWindow('Iterando...')
            return img_n
        img = img_n
        if show:
            cv2.imshow('Iterando...',img_n)
            ky = cv2.waitKey(50)
            if ky == 27:
                show = False