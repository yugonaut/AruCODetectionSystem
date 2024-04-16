from GenDect import GenDect
from PyQt5.QtWidgets import QApplication
import sys
from gui import MainWindow

def main():
    # call Class
    detector = GenDect()
    # #generate marker with default values ArucoDict_4x4_50
    # detector.generate_marker()
    # # Load Image and save it to variable img
    # img = detector.load_image("Bild5")
    # id_dict = detector.detect(img)
    # scale_factor = detector.scale(image = img, id_dict=id_dict)
    # print(scale_factor)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    



if __name__ == '__main__':
    main()