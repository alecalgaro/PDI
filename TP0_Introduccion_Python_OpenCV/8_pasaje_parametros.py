# Una biblioteca que permite el manejo del pasaje de parametros al programa es
# argparse y se debe incluir como import argparse
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import argparse

#! Recordar estar ubicado dentro de la terminal en la carpeta donde se encuentra el script
#! que se va a ejecutar, o pasarle la ruta completa del script (este archivo).
#! En este caso debo estar en la carpeta TP0_Introduccion_Python_OpenCV (me muevo con cd en la terminal)

#* Dos opciones para ejecutarlo en la terminal:
#* python 8_pasaje_parametros.py -ic imagen1.jpg
#* python 8_pasaje_parametros.py --imagen_color imagen1.jpg

# se crea el analizador de parametros y se especifican
ap = argparse.ArgumentParser()

"""
- ap.add_argument() es una función que se utiliza para especificar qué argumentos de línea de 
  comandos debe esperar el programa.
- "-ic" y "--imagen_color" son las dos formas de referirse al argumento. -ic es la forma corta y 
  --imagen_color es la forma larga. Se puede usar cualquiera de las dos cuando se ejecuta el script 
  desde la línea de comandos.
- required=True significa que este argumento es obligatorio. Si no se proporciona, el programa 
  muestra un error y se cierra.
- help es el mensaje de ayuda que se muestra cuando se ejecute el script con el argumento -h.
"""

ap.add_argument("-ic", "--imagen_color", required=True, help="path de la imagen color")

# La de abajo la dejo comentada porque si no se debe usar tambien si o si porque da error, pero se 
# podrian pasar varios parametros en el mismo comando y tener mas imagenes por ejemplo.
# ap.add_argument("-ig", "--imagen_gris", required=True, help="path de la imagen gris")

"""
    Para ejecutar el script con el argumento requerido, se debe hacerlo desde la línea de comandos 
    y proporcionar el argumento -ic o --imagen_color seguido de la ruta a la imagen. 
    Por ejemplo:
    python tu_script.py --imagen_color imagen1.jpg
    O de la forma corta: 
    python tu_script.py -ic imagen1.jpg
    Si la imagen esta en otro directorio se debe pasar la ruta completa.
"""

"""
    La línea args = vars(ap.parse_args()) es donde el script procesa los argumentos de la línea de comandos.
    Analiza los argumentos de la línea de comandos (en ap.parse_args()), luego convierte el resultado 
    en un diccionario (con vars()) y almacena ese diccionario en la variable args.
    Despues de esa linea se puede acceder a los argumentos de la línea de comandos como elementos
    del diccionario args. Por ejemplo, args["imagen_color"] nos dará la ruta a la imagen que 
    proporcionamos como argumento "imagen_color".
"""
args = vars(ap.parse_args())

#* se recuperan en variables los parametros que queremos o directamente se utilizan
nombre_imagen = args["imagen_color"]
imagen = cv2.imread(args["imagen_color"])

print("Nombre de la imagen:", nombre_imagen)
cv2.imshow('Imagen', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()