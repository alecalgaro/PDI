import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np
import cvui

import create_mask as cm
import delimit_area as da
import segment_color_rgb_image as sc

"""
El gobierno de la provincia de Misiones lo ha contratado para realizar una aplicacion que sea 
capaz de detectar zonas deforestadas. Para desarrollar un primer prototipo le han suministrado 
una imagen satelital (Deforestacion.png) en la que un experto ya delimito el area donde deberia 
existir monte nativo y sobre la cual usted debe trabajar. 

Se requiere que su aplicacion:
- Segmente y resalte en algun tono de rojo el area deforestada.
- Calcule el area total (hectareas) de la zona delimitada, el area de la zona
que tiene monte y el area de la zona deforestada.
- (Opcional) Detecte automaticamente la delimitacion de la zona.

Ayuda:
- Explore todos los canales de los diferentes modelos de color para determinar
cual (o que combinacion de ellos) le proporciona mas informacion.
- Como su objetivo es la segmentacion de las distintas zonas, piense que herramienta
(de las que ya conoce) le permitiria lograr zonas mas homogeneas.
- Utilice la referencia de la esquina inferior izquierda para computar los tamanos
de las regiones.
"""

PATH = '../images/'

def calcular_area():
    """
    Funcion para calcular el area de la zona delimitada, el area de la zona que tiene monte 
    y el area de la zona deforestada.
    """
    #! Implementar la funcion para calcular las areas, utilizando como referencia la esquina 
    #! inferior izquierda de la imagen original, donde hay una regla que mide 200m.

    # return total_area, deforested_area, forest_area

#* Cargar la imagen original
img_original = cv2.imread(PATH + 'Deforestacion.png')

#* Detectar automaticamente la delimitacion de la zona (se marca el area y se retorna los vertices)
img, vertices = da.delimit_area(img_original, 150, False)
# cv2.imshow('Imagen', img)
# print(vertices)

#* Crear mascara a partir de la zona delimitada.
#* En caso de que la funcion delimited_area no encuentre el area delimitada, por ejemplo si se
#* utiliza un umbral muy alto, la funcion create_mask recibira vertices = None y se podra seleccionar
#* manualmente la zona delimitada con el mouse.
# delimited_area sera la imagen con la zona delimitada y el resto negro
delimited_area, _ = cm.create_mask(img_original, vertices)
# cv2.imshow('Area delimitada', delimited_area)

#* Homogenizar la zona delimitada
# Se aplica un filtro de mediana para homogenizar la zona delimitada, probando diferentes tamaños
# de ventana (ksize impar) para elegir cual nos permite obtener una imagen mas homogenea en la zona
# de monte y en la zona deforestada.
ksize = 25   
filtered_area = cv2.medianBlur(delimited_area, ksize)
# cv2.imshow('Median Blur', filtered_area)

#* Segmentar el area deforestada
# Se ha probado utilizar la funcion para segmentar con rgb y con hsv, siendo en este caso 
# la mas facil de obtener un resultado optimo la segmentacion en rgb (con Rmin=71)
_, mask_segmented = sc.segment_color_rgb_image(filtered_area)

#* Aplicar color rojo a la zona deforestada
img[mask_segmented == 255] = [0, 0, 255]
delimited_area[mask_segmented == 255] = [0, 0, 255]  # para ver solo el area delimitada y deforestada

#* Mostrar y guardar las imagenes con la zona deforestada resaltada
cv2.imshow("Area deforestada", img)
cv2.imshow("Zona delimitada y deforestada", delimited_area)
cv2.imwrite(PATH + 'Deforestacion_segmentada.png', img)
cv2.imwrite(PATH + 'Deforestacion_segmentada_2.png', delimited_area)

#* Calcular el area total, el area de la zona que tiene monte y el area de la zona deforestada
# total_area, deforested_area, forest_area = calcular_area()

# print(f"Area total: {total_area} hectareas")
# print(f"Area deforestada: {deforested_area} hectareas")
# print(f"Area con monte: {forest_area} hectareas")

cv2.waitKey(0)
cv2.destroyAllWindows()