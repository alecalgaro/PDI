import cv2

def morph_fill(img,mask):
    # img --> seed point (BINARY)
    # mask --> original image to use as mask
    # process: dilate -> [img && !mask] --> repeat until img == img+1

    # Si se pasa la imagen ya en binario no hace falta hacer el threshold
    # _,mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)
    
    while True:
        k = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        img_n = cv2.morphologyEx(img, cv2.MORPH_DILATE, k, iterations = 2)
        img_n = cv2.bitwise_and(img_n, mask)
        if (img_n == img).all():
            return img_n
        img = img_n
        cv2.imshow('Iterando...',img_n)
        cv2.waitKey(50)
    cv2.destroyWindow('Iterando...')
    return img