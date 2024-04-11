import cv2
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
En el word con anotaciones deje algunas explicaciones y respuestas a las preguntas
que se hacen en el ejercicio.
"""

"""
- Visualice el patron junto a las componentes [R, G, B] y [H, S, V]

OpenCV trabaja con el modelo de color BGR, asi que puedo convertir a RGB, luego aislar las 
componentes con cv2.split() y luego crear imagenes con cv2.merge() donde solo una componente 
tiene informacion y las otras dos son cero.
"""

PATH = "../images/"

patron = cv2.imread(PATH + 'patron.tif')
patron = cv2.resize(patron, None, fx=5, fy=5)
cv2.imshow('Patron', patron)

#* --- RGB ---
# Dividir la imagen en los canales R, G y B (si quiero la puedo convertir a RGB pero da lo mismo aca)
b, g, r = cv2.split(patron)

# Para volver a generar las imagenes recordar el orden de los canales [B G R], sino las
# puedo poner en orden [R G B] pero convertirlas a BGR porque cv2.imshow() recibe una imagen BGR

# Crear una nueva imagen donde solo el canal R tiene informacion
patron_r = cv2.merge([np.zeros_like(b), np.zeros_like(g), r])

# Crear una nueva imagen donde solo el canal G tiene informacion
patron_g = cv2.merge([np.zeros_like(b), g, np.zeros_like(r)])

# Crear una nueva imagen donde solo el canal B tiene informacion
patron_b = cv2.merge([b, np.zeros_like(g), np.zeros_like(r)])

cv2.imshow('Red', patron_r)
cv2.imshow('Green', patron_g)
cv2.imshow('Blue', patron_b)

cv2.waitKey(0)
cv2.destroyAllWindows()

#? Otra opcion sin usar split y merge seria ir haciendo 0 las componentes que no queremos,
#? como muestro abajo. Ahi use los indices de BGR, azul [:,:,0], verde [:,:,1] y rojo [:,:,2]
# patron_b = patron.copy()
# patron_b[:,:,1] = 0
# patron_b[:,:,2] = 0

# patron_g = patron.copy()
# patron_g[:,:,0] = 0
# patron_g[:,:,2] = 0

# patron_r = patron.copy()
# patron_r[:,:,0] = 0
# patron_r[:,:,1] = 0

#* --- HSV --- 
# Convertir la imagen a HSV
patron_hsv = cv2.cvtColor(patron, cv2.COLOR_BGR2HSV)

patron_h = patron_hsv[:,:,0]
patron_s = patron_hsv[:,:,1]
patron_v = patron_hsv[:,:,2]

cv2.imshow('H', patron_h)    # tonos de gris representando los colores
cv2.imshow('S', patron_s)    # tonos de gris representando la saturacion
cv2.imshow('V', patron_v)    # tonos de gris representando la intensidad

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
Modique las componentes H, S y V de la imagen para obtener un patron
en RGB que cumpla con las siguientes condiciones:
- Variacion de matices de azul a rojo.
- Saturacion y brillo maximos.
"""

patron_hsv = cv2.cvtColor(patron, cv2.COLOR_BGR2HSV)

# Invierto el canal H (indice 0) para que ahora vaya de azul a rojo
patron_hsv[:,:,0] = np.flip(patron_h,1)
# Saturacion (indice 1) y brillo (indice 2) maximos
patron_hsv[:,:,1] = 255
patron_hsv[:,:,2] = 255

# Convertir la imagen de vuelta a BGR
new_img_bgr = cv2.cvtColor(patron_hsv, cv2.COLOR_HSV2BGR)

"""
Vizualice la nueva imagen y sus componentes en ambos modelos. Analice y saque conclusiones.
"""

cv2.imshow("Nueva imagen RBG", new_img_bgr)

# Dividir la nueva imagen en los canales R, G y B
b, g, r = cv2.split(new_img_bgr)
patron_r = cv2.merge([np.zeros_like(b), np.zeros_like(g), r])
patron_g = cv2.merge([np.zeros_like(b), g, np.zeros_like(r)])
patron_b = cv2.merge([b, np.zeros_like(g), np.zeros_like(r)])

cv2.imshow("Red", patron_r)
cv2.imshow("Green", patron_g)
cv2.imshow("Blue", patron_b)

# Dividir la nueva imagen en canales H, S y V
patron_hsv = cv2.cvtColor(new_img_bgr, cv2.COLOR_BGR2HSV)
patron_h = patron_hsv[:,:,0]
patron_s = patron_hsv[:,:,1]
patron_v = patron_hsv[:,:,2]

cv2.imshow("H", patron_h)   
cv2.imshow("S", patron_s)   
cv2.imshow("V", patron_v)    

cv2.waitKey(0)
cv2.destroyAllWindows()