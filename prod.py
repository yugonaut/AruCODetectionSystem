import cv2 as cv
from cv2 import aruco
import numpy as np
import matplotlib.pyplot as plt

aruco_dict = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)

fig = plt.figure()
nx = 3
ny = 5
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.generateImageMarker(aruco_dict,i, 700)
    plt.imshow(img, cmap = plt.cm.gray, interpolation = "nearest")
    ax.axis("off")

plt.savefig(r"C:\Users\damjan\Desktop\FaserProjekt\BildDetection\Plots\markers11.jpeg")
plt.show()