import cv2
import matplotlib.pyplot as plt


IMAGE_DIR = "imgs_hist/"
IMG_FILE_A = "imagenA.tif"
IMG_FILE_B = "imagenB.tif"
IMG_FILE_C = "imagenC.tif"
IMG_FILE_D = "imagenD.tif"
IMG_FILE_E = "imagenE.tif"

HIS_FILE_1 = "histo1.tif"
HIS_FILE_2 = "histo2.tif"
HIS_FILE_3 = "histo3.tif"
HIS_FILE_4 = "histo4.tif"
HIS_FILE_5 = "histo5.tif"

imagenA = cv2.imread(f"{IMAGE_DIR}{IMG_FILE_A}", cv2.IMREAD_GRAYSCALE)
imagenB = cv2.imread(f"{IMAGE_DIR}{IMG_FILE_B}", cv2.IMREAD_GRAYSCALE)
imagenC = cv2.imread(f"{IMAGE_DIR}{IMG_FILE_C}", cv2.IMREAD_GRAYSCALE)
imagenD = cv2.imread(f"{IMAGE_DIR}{IMG_FILE_D}", cv2.IMREAD_GRAYSCALE)
imagenE = cv2.imread(f"{IMAGE_DIR}{IMG_FILE_E}", cv2.IMREAD_GRAYSCALE)

histo1 = cv2.imread(f"{IMAGE_DIR}{HIS_FILE_1}", cv2.IMREAD_COLOR)
histo2 = cv2.imread(f"{IMAGE_DIR}{HIS_FILE_2}", cv2.IMREAD_COLOR)
histo3 = cv2.imread(f"{IMAGE_DIR}{HIS_FILE_3}", cv2.IMREAD_COLOR)
histo4 = cv2.imread(f"{IMAGE_DIR}{HIS_FILE_4}", cv2.IMREAD_COLOR)
histo5 = cv2.imread(f"{IMAGE_DIR}{HIS_FILE_5}", cv2.IMREAD_COLOR)

histoA = cv2.calcHist([imagenA], [0], None, [256], [0, 256])
histoB = cv2.calcHist([imagenB], [0], None, [256], [0, 256])
histoC = cv2.calcHist([imagenC], [0], None, [256], [0, 256])
histoD = cv2.calcHist([imagenD], [0], None, [256], [0, 256])
histoE = cv2.calcHist([imagenE], [0], None, [256], [0, 256])

figA, (axA1, axA2, axA3) = plt.subplots(1, 3, layout="constrained")
figA.suptitle("Imagen A", fontsize=16)
axA1.imshow(cv2.cvtColor(histo2, cv2.COLOR_BGR2RGB))
axA1.set_title("Histograma predicho")
axA2.imshow(imagenA, cmap="gray", vmax=255, vmin=0)
axA2.set_title("Imagen")
axA3.plot(histoA)
axA3.set_title("Histograma real")

figB, (axB1, axB2, axB3) = plt.subplots(1, 3, layout="constrained")
figB.suptitle("Imagen B", fontsize=16)
axB1.imshow(cv2.cvtColor(histo4, cv2.COLOR_BGR2RGB))
axB1.set_title("Histograma predicho")
axB2.imshow(imagenB, cmap="gray", vmax=255, vmin=0)
axB2.set_title("Imagen")
axB3.plot(histoB)
axB3.set_title("Histograma real")

figC, (axC1, axC2, axC3) = plt.subplots(1, 3, layout="constrained")
figC.suptitle("Imagen C", fontsize=16)
axC1.imshow(cv2.cvtColor(histo1, cv2.COLOR_BGR2RGB))
axC1.set_title("Histograma predicho")
axC2.imshow(imagenC, cmap="gray", vmax=255, vmin=0)
axC2.set_title("Imagen")
axC3.plot(histoC)
axC3.set_title("Histograma real")

figD, (axD1, axD2, axD3) = plt.subplots(1, 3, layout="constrained")
figD.suptitle("Imagen D", fontsize=16)
axD1.imshow(cv2.cvtColor(histo5, cv2.COLOR_BGR2RGB))
axD1.set_title("Histograma predicho")
axD2.imshow(imagenD, cmap="gray", vmax=255, vmin=0)
axD2.set_title("Imagen")
axD3.plot(histoD)
axD3.set_title("Histograma real")

figE, (axE1, axE2, axE3) = plt.subplots(1, 3, layout="constrained")
figE.suptitle("Imagen E", fontsize=16)
axE1.imshow(cv2.cvtColor(histo3, cv2.COLOR_BGR2RGB))
axE1.set_title("Histograma predicho")
axE2.imshow(imagenE, cmap="gray", vmax=255, vmin=0)
axE2.set_title("Imagen")
axE3.plot(histoE)
axE3.set_title("Histograma real")

plt.show()
