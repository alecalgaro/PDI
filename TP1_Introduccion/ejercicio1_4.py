import cv2
import argparse     # para pasaje de parametros

#* Para ejecutarlo recordar estar ubicado dentro de la terminal en la carpeta donde se 
#* encuentra este script, y luego ejecutar:
#* python ejercicio1_4.py -im ../images/cameraman.tif

# 4. Utilice el pasaje por parametros para especificar la imagen a cargar.
# Se explica su uso en el ejercicio 8_pasaje_parametros.py del TP0. 
# Este inciso es por si se quiere cargar la imagen desde la consola,
# para que se pueda reutilizar el código sin tener que cambiar la ruta desde el codigo.

# se crea el analizador de parametros y se especican
ap = argparse.ArgumentParser()
# se agrega el argumento
ap.add_argument("-im", "--imagen", required=True, help="path de la imagen")
# se procesan los argumentos
args = vars(ap.parse_args())
# se recuperan y usan los argumenteos obtenidos
nombre_imagen = args["imagen"]
imagen = cv2.imread(nombre_imagen)

# luego de obtener la imagen ya podria obtener informacion, dibujar arriba y los demas 
# incisos que los hicimos aparte.

# Tambien se puede cargar directamente: imagen = cv2.imread(args["imagen"])
cv2.imshow('Imagen', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()