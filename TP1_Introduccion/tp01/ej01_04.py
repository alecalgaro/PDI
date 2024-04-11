import cv2
import matplotlib.pyplot as plt
import argparse

desc="Open image passed as parameter."
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-i", "--image", dest="img", required=True,
                    help="Image file (required)")
parser.add_argument("-d", "--directory", dest="dir", default="../images/",
                    help="Images directory (../images/ by default)")
args = parser.parse_args()

imagen = cv2.imread(f"{args.dir}{args.img}", cv2.IMREAD_GRAYSCALE)

#* Matplotlib
fig, ax1 = plt.subplots(1, 1, layout="constrained")
fig.suptitle("Ej 1.4: Pasaje de parametros", fontsize=16)
ax1.imshow(imagen, cmap="gray")
ax1.set_title(f"{args.dir}{args.img}")
plt.show()
