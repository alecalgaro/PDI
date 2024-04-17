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

def calculate_reference():
    """
    Funcion para calcular los px de ancho de la imagen de referencia, correspondientes a 200 m,
    y retornar la cantidad de hectareas que representa un px en esa escala.
    """
    # Cargar la imagen con la medida de referencia
    img_reference = cv2.imread(PATH + 'Deforestacion_referencia.png')
    
    # Calcular los px de ancho de la imagen de referencia, correspondientes a 200 m
    px_width = img_reference.shape[1]
    m_width = 200   # referencia en metros

    # Calcular los px por metro segun la referencia
    m_per_px = m_width/px_width

    # Convertir a metros cuadrados y hectareas (1 ha = 10000 m^2)
    m2_per_px = m_per_px ** 2
    ha_per_px = m2_per_px / 10000

    # Retornar la cantidad de hectareas que representa un px en esa escala
    return ha_per_px

def calculate_area():
    """
    Funcion para calcular el area de la zona delimitada, el area de la zona que tiene monte 
    y el area de la zona deforestada.
    """
    
    # Calcular la cantidad de hectareas que representa un px en la escala de la imagen
    ha_per_px = calculate_reference()
    
    # Cargar la imagen con la zona delimitada y deforestada
    img = cv2.imread(PATH + 'Deforestacion_segmentada_2.png')
    
    # Calcular el area total de la zona delimitada
    # img != [0, 0, 0] devuelve una matriz booleana con True en las posiciones donde el pixel 
    # es distinto de [0, 0, 0] (negro), luego np.all(..., axis=-1) aplica la operacion all a lo largo
    # del ultimo eje (canales de color), es decir que, si todos los canales son =! 0 es True.
    # Y con np.count_nonzero(...) se cuenta el numero de True en la matriz booleana. 
    total_area = np.count_nonzero(np.all(img != [0, 0, 0], axis=-1)) * ha_per_px

    # Calcular el area de la zona no deforestada
    deforested_area = np.count_nonzero(np.all(img == [0, 0, 255], axis=-1)) * ha_per_px
    
    # Calcular el area de la zona que tiene monte
    forest_area = total_area - deforested_area

    # Redondear los valores a 2 decimales
    total_area = round(total_area, 2)
    deforested_area = round(deforested_area, 2)
    forest_area = round(forest_area, 2)

    return total_area, deforested_area, forest_area


#* Cargar la imagen original
img_original = cv2.imread(PATH + 'Deforestacion.png')

#* Detectar automaticamente la delimitacion de la zona (se marca el area y se retorna los vertices)
img, vertices = da.delimit_area(img_original, 150, False)
cv2.imshow('Identificar zona delimitada', img)
# cv2.imwrite(PATH + 'Deforestacion_area_delimitada.png', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
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
# cv2.imwrite(PATH + 'Deforestacion_zona_homogenea.png', filtered_area)

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
# cv2.imwrite(PATH + 'Deforestacion_segmentada.png', img)
# cv2.imwrite(PATH + 'Deforestacion_segmentada_2.png', delimited_area)

#* Calcular el area total, el area de la zona que tiene monte y el area de la zona deforestada
total_area, deforested_area, forest_area = calculate_area()

print(f"Area total: {total_area} hectareas")
print(f"Area deforestada: {deforested_area} hectareas")
print(f"Area con monte: {forest_area} hectareas")
print(f"Porcentaje de deforestacion: {deforested_area/total_area*100:.2f}%")

cv2.waitKey(0)
cv2.destroyAllWindows()