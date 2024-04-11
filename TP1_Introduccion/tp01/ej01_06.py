import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_images_cv(images, horiz=True, title="Images"):
    max_height = max(image.shape[0] for image in images)
    max_width = max(image.shape[1] for image in images)

    images = [cv2.resize(image, (max_width, max_height)) for image in images]

    for i in range(len(images)):
        if len(images[i].shape)<3:
            images[i]=cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGR)

    if horiz:
        stacked_image = np.hstack(images)
    else:
        stacked_image = np.vstack(images)

    while True:
        cv2.imshow(title, stacked_image)
        key = cv2.waitKey(1) & 0xFF
        # si la tecla c es presionada sale del while
        if key == ord("c"):
            cv2.destroyAllWindows()
            break


def show_images_matplotlib(images, show_axis=False, title=None,
                           ax_titles=None):
    fig, axes = plt.subplots(1, len(images), layout="constrained")
    if title is not None:
        fig.suptitle(title, fontsize=16)
    if ax_titles is not None:
        if len(ax_titles)<len(images):
            print("Warning: Missing axes titles")
            ax_titles = ax_titles + [""]*(len(images)-len(ax_titles))
    for i in range(len(images)):
        if len(images[i].shape)>2:
            axes[i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
        else:
            axes[i].imshow(images[i], cmap="gray")
        if not show_axis:
            axes[i].axis('off')
        if ax_titles is not None:
            axes[i].set_title(ax_titles[i])
    plt.show()


IMAGE_DIR = "../images/"
IMAGE_1_FILE = "futbol.jpg"
IMAGE_2_FILE = "clown.jpg"
IMAGE_3_FILE = "cameraman.tif"
imagen1 = cv2.imread(f"{IMAGE_DIR}{IMAGE_1_FILE}")
imagen2 = cv2.imread(f"{IMAGE_DIR}{IMAGE_2_FILE}", cv2.IMREAD_GRAYSCALE)
imagen3 = cv2.imread(f"{IMAGE_DIR}{IMAGE_3_FILE}")

show_images_cv([imagen1, imagen2, imagen3], title="Ej1.6: Varias imagenes")
show_images_matplotlib([imagen1, imagen2, imagen3],
                       title="Ej1.6: Varias imagenes",
                       ax_titles=[IMAGE_1_FILE, IMAGE_2_FILE, IMAGE_3_FILE])

