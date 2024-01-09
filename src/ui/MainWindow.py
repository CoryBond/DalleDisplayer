
import logging
from tkinter import *
import os

from imageProviders.ImageProvider import ImageProvider
from ui.ImageViewer import ImageViewer
from utils.dateUtils import get_current_sortable_datetime_strs
# from ui.ImageViewer import ImageViewer
from utils.pathingUtils import get_image_repos

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):


    def __init__(self, imageProvider: ImageProvider, parent=None):
        super(MainWindow, self).__init__(parent)       

        self.imageProvider = imageProvider

        self.imageRepo = self.get_engine_repo()
        if not os.path.exists(self.imageRepo):
            os.mkdir(self.imageRepo)

        self.init_ui()


    def get_engine_repo(self):
         return get_image_repos()/self.imageProvider.engine_name()


    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Full Screen UI')
        self.showFullScreen()

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

        # Add an interactable image viewer
        lastImagePosix = self.get_latest_image_posix_in_repo()
        self.imageViewer = ImageViewer(lastImagePosix)
        rootLayout.addWidget(self.imageViewer, 9)

        # S
        self.setCentralWidget(centralWidget)


    def get_latest_image_posix_in_repo(self):
        try:
            imageDates = os.listdir(self.imageRepo)
            lastImageDate = imageDates[0]
            lastDateImagePrompts = os.listdir(self.imageRepo/lastImageDate)
            lastImagePrompt = lastDateImagePrompts[0]

            lastImagePromptPosix = (self.imageRepo/lastImageDate/lastImagePrompt/"1.png").as_posix()

            logging.info("Found last image prompt of repo : " + lastImagePromptPosix)
            return lastImagePromptPosix
        except BaseException as e:
            logging.error(e)
            return None


    def generate_png_path(self, prompt: str):
        dateTimeSegments = get_current_sortable_datetime_strs()
        dayDirectory = self.imageRepo/dateTimeSegments[0]
        promptWithTime = dateTimeSegments[1] + "_" + prompt
        if not os.path.exists(dayDirectory):
            os.mkdir(dayDirectory)
        if not os.path.exists(dayDirectory/promptWithTime):
            os.mkdir(dayDirectory/promptWithTime)
        return dayDirectory/promptWithTime/"1.png"


    def on_button_click(self):
        prompt = self.inputbox.text()
        image = self.imageProvider.get_image_from_string(prompt)
        pngPath = self.generate_png_path(prompt)
        image.save(pngPath, "PNG")
        self.imageViewer.replaceimage(pngPath.as_posix())

        