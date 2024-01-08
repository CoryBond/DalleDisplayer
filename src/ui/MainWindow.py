
import logging
from tkinter import *
import os

from imageProviders.ImageProvider import ImageProvider
from ui.ImageViewer import ImageViewer
# from ui.ImageViewer import ImageViewer
from utils.pathingUtils import get_image_repos

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):


    def __init__(self, imageProvider: ImageProvider, parent=None):
        super(MainWindow, self).__init__(parent)       

        self.imageProvider = imageProvider

        self.imageFolder = get_image_repos()/imageProvider.name()

        if not os.path.exists(self.imageFolder):
            os.mkdir(self.imageFolder)

        self.init_ui()


    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Full Screen UI')
        # self.setGeometry(10, 10, 500, 500)
        self.showFullScreen()  # Full screen doesn't appear to work properly....

        # Create a vertical layout
        centralWidget = QWidget()
        rootLayout = QHBoxLayout(centralWidget)

        imageGenerationLayout = QVBoxLayout(centralWidget)

        self.inputbox = QLineEdit(self)
        imageGenerationLayout.addWidget(self.inputbox)

        # Add a button
        button = QPushButton('Generate Image', self)
        button.clicked.connect(self.on_button_click)
        imageGenerationLayout.addWidget(button)

        rootLayout.addLayout(imageGenerationLayout, 1)

        # Add an image
        self.imageViewer = ImageViewer((self.imageFolder/'test.png').as_posix())
        rootLayout.addWidget(self.imageViewer, 9)

        # S
        self.setCentralWidget(centralWidget)


    def on_button_click(self):
        image = self.imageProvider.get_image_from_string(self.inputbox.text())
        fileName = self.imageFolder/'test.png';
        image.save(self.imageFolder/'test.png', "PNG");
        self.imageViewer.replaceimage(fileName.as_posix())
        