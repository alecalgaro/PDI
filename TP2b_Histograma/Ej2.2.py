"""
Enunciado:
Realice un algoritmo de busqueda por correlacion de histogramas de intensidad.
Se debe informar el contenido de la imagen: Bandera, Caricatura, Personaje
o Paisaje. Utilice las imagenes disponibles en Busqueda histograma.zip.
"""

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import matplotlib.pyplot as plt

PATH = "../images/Busqueda_histograma/"

"""
Investigando se llego a:
-Comparar histogramas directamente puede ser útil si las imágenes son muy similares en color y tono. 
Sin embargo, este enfoque puede ser sensible a variaciones en la iluminación y otros factores que 
pueden cambiar el histograma de una imagen sin cambiar su contenido significativamente.

-Por otro lado, calcular propiedades estadísticas de los histogramas puede proporcionar una 
representación más robusta. La media y la varianza pueden capturar información sobre el brillo y 
el contraste de la imagen, respectivamente. La asimetría puede capturar información sobre si los 
colores de la imagen están sesgados hacia el brillo o la oscuridad. La energía puede capturar 
información sobre la uniformidad de los colores en la imagen, y la entropía puede capturar 
información sobre la complejidad o la cantidad de información en la imagen.

-Dado que tenemos distintostipos de imágenes (banderas, caricaturas, personas y paisajes), 
seria recomendable calcular las propiedades estadísticas de los histogramas y usar esas propiedades 
para comparar, y asi tener una representación más robusta y flexible para la variedad de imágenes.
"""

"""
Cosas para pensar:

-Las banderes tienen pocos colores y todos uniformes, por lo tanto, en escala de grises van a ser
pocos niveles de grises que van a representar pocos picos en el histograma y altos.

-Las caricaturas también tienen colores uniformes, así que tendrán varios picos en el histograma 
y el resto del histograma todo en 0 o cerca de 0. Y suelen tener un fondo fijo (generalmente blanco),
asi que el histograma va a tener un pico alto en ese color.

-Las imagenes de paisajes son todas playas asi que tienen mas o menos los mismos colores.
"""

import cv2
import numpy as np
import Statistics_functions as sf

# Función para calcular y graficar el histograma de una imagen
def plot_histogram(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    hist = cv2.calcHist([image], [0], None, [256], [0,256])
    plt.figure()
    plt.plot(hist)
    plt.title('Histograma de ' + image_path)
    
# Función para calcular las propiedades estadisticas de un histograma
def calculate_stats(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    hist = cv2.calcHist([image], [0], None, [256], [0,256])
    mean = sf.media(hist)
    var = sf.varianza(hist)
    skewness = sf.asimetria(hist)
    energy = sf.energia(hist)
    ent = sf.entropia(hist)
    return [mean, var, skewness, energy, ent]

# Función para clasificar imágenes en categorías
def classify_images(representative_images, image_files):
    representative_stats = {}

    # Calcular las estadísticas de las imágenes representativas y graficar histogramas
    for category, image_name in representative_images.items():
        representative_stats[category] = calculate_stats(PATH + image_name)
        plot_histogram(PATH + image_name)
    plt.show()  # Muestra los histogramas de las imágenes representativas

    # Clasificar las imágenes en el conjunto de datos
    for image_file in image_files:
        image_stats = calculate_stats(PATH + image_file)
        
        # Calcula la distancia a las imágenes representativas (si ord=2 es la distancia euclideana)
        distances = {}
        for category, stats in representative_stats.items():
            distances[category] = np.linalg.norm(np.array(image_stats) - np.array(stats), ord=2)

        # Asigna la imagen a la categoría con la menor distancia
        category = min(distances, key=distances.get)
        print(f"La imagen {image_file} se clasifica como {category}")

"""
Se debe crear un diccionario con la imagen representativa para cada categoria, las cuales se 
usarán para calcular las propiedades estadísticas y comparar luego con el listado de imagenes 
que se desea clasificar.
"""

# Imágenes representativas para cada categoría
representative_images = {"Bandera": "Bandera04.jpg", 
                         "Caricatura": "Caricaturas01.jpg", 
                         "Personaje": "Personaje03.jpg", 
                         "Paisaje": "Paisaje02.jpg"
                         }

# Listado de imágenes a clasificar
image_files = ["Bandera02.jpg", "Bandera03.jpg", "Bandera04.jpg", "Bandera04.jpg",
               "Caricaturas02.jpg", "Caricaturas03.jpg", "Caricaturas04.jpg", "Caricaturas05.jpg",
               "Personaje02.jpg", "Personaje03.jpg", "Personaje04.jpg", "Personaje05.jpg",
               "Paisaje02.jpg", "Paisaje03.jpg", "Paisaje04.jpg", "Paisaje05.jpg"
               ]

# Clasificar las imágenes
classify_images(representative_images, image_files)