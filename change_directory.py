"""
Debajo dejo dos lineas para cambiar el directorio de trabajo al directorio donde se encuentra el script.
Me sirve para usar rutas como en "PATH" que son relativas a la ubicacion del script y no tener problema
por ejemplo si abro VSC desde la carpeta general con otras carpetas o desde la carpeta propia del script.
Puedo copiar y pegar esas dos lineas siempre en los ejercicios.
"""
import os
# Cambia el directorio de trabajo al directorio donde se encuentra el script
os.chdir(os.path.dirname(os.path.abspath(__file__)))