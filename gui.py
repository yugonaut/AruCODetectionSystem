import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
from GenDect import GenDect
import cv2 as cv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aruco Marker Detection")
        self.setGeometry(100, 100, 800, 600)

        self.detector = GenDect()
        self.file_path = None

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)     

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image files (*.jpg *.png)")
        if file_path:
            self.image = self.detector.load_image(file_path)
            self.process_image(self.image)
    
    def process_image(self, image):
        self.id_dict = self.detector.detect(image)
        self.scale = self.detector.scale(id_dict = self.id_dict, image = self.image)
        print(self.scale)

