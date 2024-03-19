import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import numpy as np

image = cv2.imread("futbol.jpg")

# Create a new image the zeros with the same dimensions and data type as the original image
new_image = np.zeros(image.shape, dtype=image.dtype)
cv2.imshow("Nueva imagen", new_image)

# Another option
new_image2 = np.zeros_like(image)

# Load the image in grayscale
gray_image = cv2.imread("futbol.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("Imagen en escala de grises", gray_image)

# Another option converting from BGR to GRAY
gray_image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Otra imagen en escala de grises", gray_image2)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the image
cv2.imwrite("futbol_gris.jpg", gray_image)