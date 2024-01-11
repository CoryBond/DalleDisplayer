import logging
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDialog, QDialogButtonBox, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from speechRecognition.SpeechRegonizer import SpeechRecognizer
from utils.pathingUtils import get_or_create_image_resources


class RecorderDialog(QDialog):
    # Becaues QT widgets can't be updated via multi-threading... but Signals + Slots are thread safe we use that to communicate between the speech recognizer and this dialog
    transcribeEvent = pyqtSignal()

    def __init__(self, speechRecognizer: SpeechRecognizer):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.speechRecognizer = speechRecognizer
        self.stop_transcribing = lambda : None

        self.init_ui()

        self.transcribeEvent.connect(self.updateTranscriptionBox)
        self.stop_transcribing = speechRecognizer.transcribe(notify=lambda : self.transcribeEvent.emit())


    def init_ui(self):
        self.layout = QVBoxLayout()

        self.contentLayout = QHBoxLayout()

        recorderPixmap = QPixmap((get_or_create_image_resources()/"preview.png").as_posix())
        recorderLabel = QLabel()
        recorderLabel.setPixmap(recorderPixmap)
        self.contentLayout.addWidget(recorderLabel)

        messageLayout = QVBoxLayout()
        message = QLabel("Please record your voice now!")
        message2 = QLabel("Once \"accepted\" the voice will replace the current prompt.")
        self.transcriptionBox = QTextEdit(self)
        self.transcriptionBox.setDisabled(True)
        messageLayout.addWidget(message)
        messageLayout.addWidget(message2)
        messageLayout.addWidget(self.transcriptionBox)
        self.contentLayout.addLayout(messageLayout)

        self.layout.addLayout(self.contentLayout)

        QBtn = QDialogButtonBox.Ok  | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.acceptTranscription)
        self.buttonBox.rejected.connect(self.rejectTranscription)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    
    def updateTranscriptionBox(self):
        logging.info("got transcription update")
        self.transcriptionBox.setText(self.speechRecognizer.get_transcription())


    def acceptTranscription(self):
        logging.info("accepted dialog")
        self.stop_transcribing(wait_for_stop=False)
        self.trascription = self.speechRecognizer.get_transcription()
        self.accept()


    def rejectTranscription(self):
        logging.info("rejected dialog")
        self.stop_transcribing(wait_for_stop=False)
        self.reject()