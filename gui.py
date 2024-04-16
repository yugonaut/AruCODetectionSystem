import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget,QLineEdit, QGridLayout
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

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)
        titles = ["Number 1:", "Number 2:", "Number 3:", "Number 4:", "Number 5:", "Number 6:"]
        self.number_inputs = []
        for i, title in enumerate(titles):
            label = QLabel(title)
            grid_layout.addWidget(label, i // 2, i % 2 * 2)

            number_input = QLineEdit()
            grid_layout.addWidget(number_input, i // 2, i % 2 * 2 + 1)
            self.number_inputs.append(number_input)

        save_button = QPushButton('Save Numbers', self)
        save_button.clicked.connect(self.save_numbers)
        layout.addWidget(save_button)

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

    def save_numbers(self):
        numbers = [input.text() for input in self.number_inputs]
        print("Numbers:", numbers)  # You can save or process the numbers here