import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

#? 6. Investigue y realice una funcion que le permita mostrar varias imagenes en una sola ventana.

PATH = "../images/"

image1 = cv2.imread(PATH + "cameraman.tif")
image2 = cv2.imread(PATH + "flores02.jpg")

#* Funcion que permite mostrar varias imagenes en distintas ventanas
def show_images_different_windows(images, titles):
    for i in range(len(images)):
        cv2.imshow(titles[i], images[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

show_images_different_windows([image1, image2], ['Cameraman', 'Flores'])

#* Funcion que permite mostrar varias imagenes en una sola ventana
def show_images_same_windows(images):
    # Tomar el alto y ancho maximo entre todas las imagenes
    max_height = max(image.shape[0] for image in images)
    max_width = max(image.shape[1] for image in images)

    # Redimensionar las imagenes para que todas tengan el mismo tamaño
    images = [cv2.resize(image, (max_width, max_height)) for image in images]

    # Apilar las imagenes horizontalmente con np.hstack
    stacked_image = np.hstack(images)
    # Aplicar las imagenes verticalmente con np.vstack
    # stacked_image = np.vstack(images)

    # Mostrar las imagenes apiladas en una misma ventana
    cv2.imshow('Images', stacked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

show_images_same_windows([image1, image2])

#* Funcion para mostrar varias imagenes en la misma ventana, utilizando matplotlib.pyplot
import matplotlib.pyplot as plt

def show_images_same_windows_matplotlib(images):
    # plt.figure(figsize=(10, 10)) # si se quiere dar un tamaño a la figura
    plt.figure()
    for i in range(len(images)):
        plt.subplot(1, len(images), i+1)
        # para mostrarlas se debe convertir las imagenes de BGR a RGB porque matplotlib usa RGB y cv2 usa BGR
        plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
        plt.axis('off') # si no se quiere mostrar los ejes ni numeros
    plt.show()

show_images_same_windows_matplotlib([image1, image2])

# Otra forma usando axes en vez de plt.subplot
def show_images_same_windows_matplotlib2(images):
    fig, axes = plt.subplots(1, len(images))
    for i in range(len(images)):
        axes[i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
        axes[i].axis('off')  
    plt.show()

show_images_same_windows_matplotlib2([image1, image2])

# Cuando creas subtramas con plt.subplots, te devuelve una referencia a la figura y a los "axes". 
# En este caso, axes es una lista de objetos "Axe", uno para cada subtrama. Cada objeto "Axe" tiene 
# métodos para trazar datos, configurar etiquetas de ejes, títulos, etc.