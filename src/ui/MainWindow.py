import logging
from imageProviders.ImageProvider import ImageProvider
from repoManager.RepoManager import RepoManager
from speechRecognition.SpeechRegonizer import SpeechRecognizer
from ui.ImageViewer import ImageViewer

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QVBoxLayout, QTextEdit, QWidget, QGroupBox, QDialog

from ui.RecorderDialog import RecorderDialog

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

        imageGenerationLayout.addWidget(self.createPromptCreator())

        # Add a button
        imageGenerationLayout.addLayout(self.createImageButtons(centralWidget))

        rootLayout.addLayout(imageGenerationLayout, 1)

        # Add an interactable image viewer
        lastImagePosix = self.repoManager.get_latest_image_posix_in_repo()
        self.imageViewer = ImageViewer(lastImagePosix)
        rootLayout.addWidget(self.imageViewer, 9)

        # S
        self.setCentralWidget(centralWidget)

        # Trigger the action that happens when the prompt box is empty
        self.prompt_text_changed_action()


    def createPromptCreator(self) -> QWidget:
        promptCreatorBox = QGroupBox("Create Your Prompt Below")
        promptBoxLayout = QVBoxLayout()

        self.promptbox = QTextEdit(self)
        self.promptbox.textChanged.connect(self.prompt_text_changed_action)

        self.promptbox.setFixedHeight(100)
        promptBoxLayout.addWidget(self.promptbox)
        promptBoxLayout.addLayout(self.createPromptButtons())

        self.clearPrompt = QPushButton('Clear Prompt', self)
        self.clearPrompt.setStyleSheet("background-color: red")
        self.clearPrompt.clicked.connect(lambda : self.promptbox.clear())
        promptBoxLayout.addWidget(self.clearPrompt)

        promptCreatorBox.setLayout(promptBoxLayout)
        return promptCreatorBox


    def createPromptButtons(self) -> QHBoxLayout:
        buttonLayout = QHBoxLayout()

        recordVoiceButton = QPushButton('Replace With Voice Input', self)
        recordVoiceButton.clicked.connect(self.record_voice_action)

        buttonLayout.addWidget(recordVoiceButton)

        return buttonLayout


    def createImageButtons(self, centralWidget) -> QHBoxLayout:
        buttonLayout = QHBoxLayout(centralWidget)

        self.generateImageButton = QPushButton('Generate Image', self)
        self.generateImageButton.clicked.connect(self.create_image_action)
        self.generateImageButton.setStyleSheet("background-color: green; height: 80px")

        buttonLayout.addWidget(self.generateImageButton)

        return buttonLayout


    def toggle_disabled_prompting(self, flag: bool):
        self.generateImageButton.setDisabled(flag)
        self.clearPrompt.setDisabled(flag)


    def create_image_action(self):
        self.toggle_disabled_prompting(True)
        prompt = self.promptbox.toPlainText()
        image = self.imageProvider.get_image_from_string(prompt)
        pngPath = self.repoManager.save_image(prompt, image)
        self.imageViewer.replaceimage(pngPath.as_posix())
        self.toggle_disabled_prompting(False)


    def record_voice_action(self):
        dlg = RecorderDialog(self.speechRecognizer)
        if dlg.exec():
            logging.info("Recorder Dialog Succeeded with transcription: " + dlg.trascription)
            self.promptbox.setText(dlg.trascription)

        
    def prompt_text_changed_action(self):
        isEmptyText = self.promptbox.toPlainText() is ""
        self.toggle_disabled_prompting(isEmptyText)
