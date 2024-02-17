import logging
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QVBoxLayout, QTextEdit, QWidget, QGroupBox
from PyQt5.QtCore import pyqtSignal

from speechRecognition.SpeechRegonizer import SpeechRecognizer
from ui.dialogs.RecorderDialog import RecorderDialog


class ImageGenerator(QWidget):
    """
    QT Widget to allow users to make the prompt used to generate images.

    Attributes
    ----------

    Methods
    ----------

    """
    def __init__(self, createImageSignal: pyqtSignal, speechRecognizer: SpeechRecognizer):
        super().__init__()


        self.speechRecognizer = speechRecognizer
        self.createImageSignal = createImageSignal

        self.init_ui()


    def init_ui(self):

        imageGenerationLayout = QVBoxLayout()

        imageGenerationLayout.addWidget(self.createPromptCreator())
        imageGenerationLayout.addLayout(self.createImageButtons())

        self.setLayout(imageGenerationLayout)


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

        self.recordVoiceButton = QPushButton('Replace With Voice Input', self)
        self.recordVoiceButton.clicked.connect(self.record_voice_action)

        buttonLayout.addWidget(self.recordVoiceButton)

        return buttonLayout


    def createImageButtons(self) -> QHBoxLayout:
        buttonLayout = QHBoxLayout()

        self.generateImageButton = QPushButton('Generate Image', self)
        self.generateImageButton.clicked.connect(self.create_image_action)
        self.generateImageButton.setStyleSheet("background-color: green; height: 80px")

        buttonLayout.addWidget(self.generateImageButton)

        return buttonLayout


    def toggle_disabled_prompting(self, flag: bool):
        self.generateImageButton.setDisabled(flag)
        self.clearPrompt.setDisabled(flag)
        self.promptbox.setDisabled(flag)
        self.recordVoiceButton.setDisabled(flag)


    def create_image_action(self):
        self.toggle_disabled_prompting(True)
        # self.loadingScreen.showWithAnimation()
        prompt = self.promptbox.toPlainText()
        self.createImageSignal.emit(prompt)


    def record_voice_action(self):
        dlg = RecorderDialog(self.speechRecognizer)
        if dlg.exec():
            logging.info("Recorder Dialog Succeeded with transcription: " + dlg.trascription)
            self.promptbox.setText(dlg.trascription)

        
    def prompt_text_changed_action(self):
        isEmptyText = self.promptbox.toPlainText() == ""
        self.generateImageButton.setDisabled(isEmptyText)
        self.clearPrompt.setDisabled(isEmptyText)