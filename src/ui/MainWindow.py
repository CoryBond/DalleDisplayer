
import logging
from tkinter import *

from imageProviders.ImageProvider import ImageProvider
from repoManager.RepoManager import RepoManager
from speechRecognition.SpeechRegonizer import SpeechRecognizer
from ui.ImageViewer import ImageViewer

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):


    def __init__(self, imageProvider: ImageProvider, repoManager: RepoManager, speechRecognizer: SpeechRecognizer, parent=None):
        super(MainWindow, self).__init__(parent)       

        self.imageProvider = imageProvider
        self.speechRecognizer = speechRecognizer
        self.repoManager = repoManager

        self.init_ui()


    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Full Screen UI')
        self.showFullScreen()

        # Create a vertical layout
        centralWidget = QWidget()
        rootLayout = QHBoxLayout(centralWidget)

        imageGenerationLayout = QVBoxLayout(centralWidget)

        self.inputbox = QLineEdit(self)
        self.inputbox.setFixedHeight(300)
        imageGenerationLayout.addWidget(self.inputbox)

        # Add a button
        imageGenerationLayout.addLayout(self.createImageButtons(centralWidget))

        rootLayout.addLayout(imageGenerationLayout, 1)

        # Add an interactable image viewer
        lastImagePosix = self.repoManager.get_latest_image_posix_in_repo()
        self.imageViewer = ImageViewer(lastImagePosix)
        rootLayout.addWidget(self.imageViewer, 9)

        # S
        self.setCentralWidget(centralWidget)


    def createImageButtons(self, centralWidget) -> QHBoxLayout:
        buttonLayout = QHBoxLayout(centralWidget)

        generateImageButton = QPushButton('Generate Image', self)
        generateImageButton.clicked.connect(self.create_image_action)

        recordVoiceButton = QPushButton('Record Voice Input', self)
        recordVoiceButton.clicked.connect(self.record_voice_action)

        buttonLayout.addWidget(generateImageButton)
        buttonLayout.addWidget(recordVoiceButton)

        return buttonLayout


    def create_image_action(self):
        prompt = self.inputbox.text()
        image = self.imageProvider.get_image_from_string(prompt)
        pngPath = self.repoManager.save_image(prompt, image)
        self.imageViewer.replaceimage(pngPath.as_posix())


    def record_voice_action(self):
        transcription = self.speechRecognizer.transcribe()
        self.inputbox.setText(transcription)

        