import cv2 as cv
from cv2 import aruco
import numpy as np
import matplotlib.pyplot as plt

arucoDict = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
img = cv.imread(r"C:\Users\damjan\Desktop\FaserProjekt\BildDetection\Bilder\benj.jpg")
cv.namedWindow("Image", cv.WINDOW_NORMAL)
cv.imshow("Image", img)     

aruco_params = aruco.DetectorParameters()
(corners, ids, rejected) = aruco.detectMarkers(image=img, dictionary= arucoDict, parameters= aruco_params)
id_dict = {}


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
		id_dict[markerID] = [cX, cY]

		cv.circle(img, (cX, cY), 4, (0, 0, 255), -1)
		# draw the ArUco marker ID on the image
		cv.putText(img, str(markerID),
			(topLeft[0], topLeft[1] - 15), cv.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
		print("[INFO] ArUco marker ID: {}".format(markerID))
		# show the output image
cv.imshow("Image", img)
cv.waitKey(0)

#Mittelpunkte der Skalierungspunkte
cv.circle(img, (id_dict[9][0], id_dict[9][1]), 4, (0, 0, 255), -1)
cv.circle(img, (id_dict[10][0], id_dict[10][1]), 4, (0, 0, 255), -1)
cv.circle(img, (id_dict[11][0], id_dict[11][1]), 4, (0, 0, 255), -1)
cv.circle(img, (id_dict[12][0], id_dict[12][1]), 4, (0, 0, 255), -1)

#Linie verbindet die skalierungspunkte
cv.line(img, id_dict[9], id_dict[10], (0, 255, 0), 2)
cv.line(img, id_dict[11], id_dict[12], (0, 255, 0), 2)

#Bild zeigen
cv.imshow("Image", img)
cv.waitKey(0)

#berechnung der länge der skalierungsgeraden
length1_px = np.sqrt(((id_dict[9][0]-id_dict[10][0])**2)+((id_dict[9][1]-id_dict[10][1])**2))
length2_px = np.sqrt(((id_dict[11][0]-id_dict[12][0])**2)+((id_dict[11][1]-id_dict[12][1])**2))

#skalierungsfaktor reale distanz in cm durch gemessenen pixel auf bild
scale_factor1 = 15.4/length1_px#[cm/px]
scale_factor2 = 21.4/length2_px
scale_factor = np.mean([scale_factor1, scale_factor2])
 
length_px = np.sqrt(((id_dict[13][0]-id_dict[14][0])**2)+((id_dict[13][1]-id_dict[14][1])**2))	

print(length_px*scale_factor)