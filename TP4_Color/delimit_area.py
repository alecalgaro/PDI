import cv2
import numpy as np

def delimit_area(image, umbral, graph=False):
    """
    Funcion para delimitar una zona de una imagen utilizando perfiles de intensidad 
    horizontal, vertical y un umbral dado.

    Se recibe una imagen, un umbral de intensidad para encontrar la zona delimitada y un booleano
    para indicar si se quiere dibujar el recuadro en la imagen (opcional).
    Se devuelve la imagen con el recuadro interno dibujado y un arreglo con los vertices del mismo.
    """
    
    #* Si se quiere calcular los perfiles de intensidad promedio de izquierda a derecha y de arriba a abajo
    # Al ser el promedio de todos los px a lo largo de cada eje, es robusto a variaciones en la
    # ubicacion de la zona a delimitar. Mientras que si se calcula por ejemplo en la mitad de la
    # imagen, antes hay que asegurarse de que la zona a delimitar este en esa ubicacion.
    # perfil_horizontal = np.mean(image, axis=0)
    # perfil_vertical = np.mean(image, axis=1)

    #* Si se quiere calcular los perfiles de intensidad en la mitad de la imagen
    # En los casos donde tenemos la imagen y podemos asumir que la zona a delimitar esta en el 
    # centro de la imagen, podemos calcular los perfiles de intensidad en la mitad de cada eje.
    mid_height = image.shape[0] // 2    # division entera
    mid_width = image.shape[1] // 2
    perfil_horizontal = image[mid_height, :]
    perfil_vertical = image[:, mid_width]

    # Encontrar donde el perfil de intensidad supera un cierto umbral dado
    indices_horizontal = np.where(perfil_horizontal > umbral)[0]
    indices_vertical = np.where(perfil_vertical > umbral)[0]

    # Comprobar que los arrays no esten vacios antes de acceder a sus elementos
    if indices_horizontal.size > 0 and indices_vertical.size > 0:
        # Encontrar los extremos externos del recuadro
        x1_ext = indices_horizontal[0]
        x2_ext = indices_horizontal[-1]
        y1_ext = indices_vertical[0]
        y2_ext = indices_vertical[-1]

        # Encontrar donde el perfil de intensidad cae por debajo del umbral dentro del recuadro
        # para encontrar los extremos internos del recuadro en caso de que el recuadro tenga varios pixeles de borde
        indices_horizontal_int = np.where(perfil_horizontal[x1_ext:x2_ext] < umbral)[0]
        indices_vertical_int = np.where(perfil_vertical[y1_ext:y2_ext] < umbral)[0]

        # Encontrar los extremos internos del recuadro
        x1_int = x1_ext + indices_horizontal_int[0]
        x2_int = x1_ext + indices_horizontal_int[-1]
        y1_int = y1_ext + indices_vertical_int[0]
        y2_int = y1_ext + indices_vertical_int[-1]

        # Si como parametro se indica que se quiere dibujar el recuadro en la imagen
        # Si se quiere dibujar el recuadro externo, se debe usar las coordenadas x1_ext, x2_ext, y1_ext, y2_ext
        if(graph):
            cv2.rectangle(image, (x1_int, y1_int), (x2_int, y2_int), (0, 255, 0), 2)

        # Mostrar la imagen
        # cv2.imshow('Imagen', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Devolver la imagen con el recuadro interno dibujado y un arreglo con los vertices del recuadro
        return image, [(x1_int, y1_int), (x2_int, y1_int), (x2_int, y2_int), (x1_int, y2_int)]

    else:
        print("No se encontró un recuadro con el umbral dado.")
        return None, None