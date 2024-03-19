import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import matplotlib.pyplot as plt

# Declarar una figura
plt.figure()

# Cargar una imagen en la figura
image = cv2.imread("futbol.jpg")
plt.imshow(image)
plt.show()

# Imagen en escala de grises
# image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Asignar falsos colores a imagenes en escala de grises
# (No me quedo claro para que es eso)
# plt.imshow(image_grey, cmap='gray')
# plt.show()

# Utilizar subfiguras con plt.subplot(num_rows, num_cols, actual)
# Comentar el imshow de arriba porque sino va a aparecer ese y luego este subplot 
# plt.subplot(1, 3, 1)
# plt.imshow(image)
# plt.subplot(1, 3, 2)
# plt.imshow(image_grey, cmap='gray')
# plt.subplot(1, 3, 3)
# plt.imshow(image)
# plt.show()

"""
De esa manera de arriba uso los subplots individuales uno por uno con plt.subplot(...).
Otra forma de hacer el subplot es:
fig, axs = plt.subplots(2, 2)
axs[0,0].imshow(img, cmap='gray')   # para mostrar una imagen
axs[0,0].set_title('Imagen original')   # para poner un título
axs[1,0].imshow(img_eq, cmap='gray')
axs[0,1].plot(hist)     # para mostrar un gráfico
axs[1,1].plot(hist_eq)
plt.show()

Donde fig es la figura y axs es un array de subfiguras.
Cada elemento de axs[] es un objeto Axes que representa un subplot individual en la figura, 
donde puedo dibujar gráficos o imágenes.
Tiene la ventaja de que puedo hacer un subplot de una vez y usar el array de Axes y no uno por uno.
"""