import cv2 as cv
from cv2 import aruco
import numpy as np
import matplotlib.pyplot as plt

arucoDict = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
img = cv.imread(r"C:\Users\damjan\Desktop\FaserProjekt\BildDetection\Bilder\benj.jpg")

aruco_params = aruco.DetectorParameters()
(corners, ids, rejected) = aruco.detectMarkers(image=img, dictionary= arucoDict, parameters= aruco_params)


if len(corners) > 0:
	# flatten the ArUco IDs list
	ids = ids.flatten()
	print(ids)
	# loop over the detected ArUCo corners
	for (markerCorner, markerID) in zip(corners, ids):
		# extract the marker corners (which are always returned in
		# top-left, top-right, bottom-right, and bottom-left order)
		corners = markerCorner.reshape((4, 2))
		(topLeft, topRight, bottomRight, bottomLeft) = corners
		# convert each of the (x, y)-coordinate pairs to integers
		topRight = (int(topRight[0]), int(topRight[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))
		
		# draw the bounding box of the ArUCo detection
		cv.line(img, topLeft, topRight, (0, 255, 0), 2)
		cv.line(img, topRight, bottomRight, (0, 255, 0), 2)
		cv.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
		cv.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
		# compute and draw the center (x, y)-coordinates of the ArUco
		# marker
		cX = int((topLeft[0] + bottomRight[0]) / 2.0)
		cY = int((topLeft[1] + bottomRight[1]) / 2.0)
		cv.circle(img, (cX, cY), 4, (0, 0, 255), -1)
		# draw the ArUco marker ID on the image
		cv.putText(img, str(markerID),
			(topLeft[0], topLeft[1] - 15), cv.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
		print("[INFO] ArUco marker ID: {}".format(markerID))
		# show the output image
cv.imshow("Image", img)
cv.waitKey(0)