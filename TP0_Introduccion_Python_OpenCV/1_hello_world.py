import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2

# Load the image, show its dimensions and data type
image = cv2.imread("futbol.jpg")
print("Dimensiones de la imagen: ", image.shape)
print("Tipo de dato de la imagen: ", image.dtype)

# display the image in a window and destroy the window when a key is pressed
cv2.imshow("Imagen", image)
cv2.waitKey(0)
cv2.destroyAllWindows()