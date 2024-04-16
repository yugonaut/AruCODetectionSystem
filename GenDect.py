import cv2 as cv
from cv2 import aruco
import numpy as np
import matplotlib.pyplot as plt
from ArucoDicts import arucoDict

class GenDect:
    def __init__(self, n = 4, m = 50, scale_point_1 = 9, scale_point_2 = 10, scale_point_3 = 11, scale_point_4 = 12):
        aruco_dict_import = arucoDict()
        self.n = n
        self.m = m
        self.aruco_markername = aruco_dict_import[f"DICT_{self.n}X{self.n}_{self.m}"]


    def generate_marker(self, save_name = "ArucoBoard"):
        
        aruco_dict = aruco.getPredefinedDictionary(self.aruco_markername)

        fig = plt.figure()
        nx = 4
        ny = 3
        for i in range(1, nx*ny+1):
            ax = fig.add_subplot(ny,nx, i)
            img = aruco.generateImageMarker(aruco_dict,i, 700)
            plt.imshow(img, cmap = plt.cm.gray, interpolation = "nearest")
            ax.axis("off")

        plt.savefig(rf"C:\Users\damjan\Desktop\FaserProjekt\BildDetection\Plots\{save_name}.jpeg")
        

    def load_image(self, image_path):
        img = cv.imread(f"{image_path}")
        cv.namedWindow("Image", cv.WINDOW_NORMAL)
        cv.imshow("Image", img)     

        return img
    
    def detect(self, image):
        arucoDict = aruco.getPredefinedDictionary(self.aruco_markername)
        aruco_params = aruco.DetectorParameters()
        (corners, ids, rejected) = aruco.detectMarkers(image=image, dictionary= arucoDict, parameters= aruco_params)
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
                cv.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv.line(image, topRight, bottomRight, (0, 255, 0), 2)
                cv.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                # compute and draw the center (x, y)-coordinates of the ArUco
                # marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                id_dict[markerID] = [cX, cY]

                cv.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                # draw the ArUco marker ID on the image
                cv.putText(image, str(markerID),
                    (topLeft[0], topLeft[1] - 15), cv.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                print("[INFO] ArUco marker ID: {}".format(markerID))
                # show the output image
        cv.imshow("Image", image)
        cv.waitKey(0)
        return id_dict
    
    def scale(self, image, id_dict):
        #Mittelpunkte der Skalierungspunkte
        cv.circle(image, (id_dict[9][0], id_dict[9][1]), 4, (0, 0, 255), -1)
        cv.circle(image, (id_dict[10][0], id_dict[10][1]), 4, (0, 0, 255), -1)
        cv.circle(image, (id_dict[11][0], id_dict[11][1]), 4, (0, 0, 255), -1)
        cv.circle(image, (id_dict[12][0], id_dict[12][1]), 4, (0, 0, 255), -1)

        #Linie verbindet die skalierungspunkte
        cv.line(image, id_dict[9], id_dict[10], (0, 255, 0), 2)
        cv.line(image, id_dict[11], id_dict[12], (0, 255, 0), 2)

        #Bild zeigen
        cv.imshow("Image", image)
        cv.waitKey(0)

        #berechnung der länge der skalierungsgeraden
        length1_px = np.sqrt(((id_dict[9][0]-id_dict[10][0])**2)+((id_dict[9][1]-id_dict[10][1])**2))
        length2_px = np.sqrt(((id_dict[11][0]-id_dict[12][0])**2)+((id_dict[11][1]-id_dict[12][1])**2))

        #skalierungsfaktor reale distanz in cm durch gemessenen pixel auf bild
        scale_factor1 = 15.4/length1_px#[cm/px]
        scale_factor2 = 21.4/length2_px
        scale_factor = np.mean([scale_factor1, scale_factor2])

        return scale_factor
    
    
