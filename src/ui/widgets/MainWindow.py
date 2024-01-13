import logging
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QVBoxLayout, QTextEdit, QWidget, QGroupBox
from PyQt5.QtCore import Qt, pyqtSignal, QRunnable, QThreadPool

from imageProviders.ImageProvider import ImageProvider, ImageProviderResult
from repoManager.RepoManager import RepoManager
from speechRecognition.SpeechRegonizer import SpeechRecognizer
from ui.dialogs.LoadingPopup import LoadingPopup
from ui.widgets.ImageViewer import ImageViewer
from ui.dialogs.RecorderDialog import RecorderDialog
from ui.dialogs.ErrorMessage import ErrorMessage


class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)


def background_create_image_process(imageProvider: ImageProvider, prompt: str, signal: pyqtSignal(str, object)):
    response = imageProvider.get_image_from_string(prompt)
    signal.emit(prompt, response)


class MainWindow(QMainWindow):
    loadImageSignal = pyqtSignal(str, object)

    def __init__(self, imageProvider: ImageProvider, repoManager: RepoManager, speechRecognizer: SpeechRecognizer, parent=None):
        super(MainWindow, self).__init__(parent)               

        # Multi-threading tasks
        self.threadpool = QThreadPool()

        self.imageProvider = imageProvider
        self.speechRecognizer = speechRecognizer
        self.repoManager = repoManager

        self.init_ui()


    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Full Screen UI')
        self.showFullScreen()

        # Pre-load common popups so there isn't a delay when they show up
        self.loadingScreen = LoadingPopup()

        self.loadImageSignal.connect(self.load_image_response, Qt.QueuedConnection)

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

        self.recordVoiceButton = QPushButton('Replace With Voice Input', self)
        self.recordVoiceButton.clicked.connect(self.record_voice_action)

        buttonLayout.addWidget(self.recordVoiceButton)

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
        self.promptbox.setDisabled(flag)
        self.recordVoiceButton.setDisabled(flag)


    def create_image_action(self):
        self.toggle_disabled_prompting(True)
        self.loadingScreen.showWithAnimation()
        prompt = self.promptbox.toPlainText()

        imageGenerationProcess = ProcessRunnable(target=background_create_image_process, args=(self.imageProvider, prompt, self.loadImageSignal))
        self.threadpool.start(imageGenerationProcess)


    def load_image_response(self, prompt: str, response: ImageProviderResult):        
        if response['errorMessage'] != None:
            # Remove loading Screen so it doesn't overlap the error message
            self.loadingScreen.stop()
            ErrorMessage(response['errorMessage']).exec()
        else:
            pngPath = self.repoManager.save_image(prompt, response['img'])
            self.imageViewer.replaceimage(pngPath.as_posix())
        
        self.loadingScreen.stop()
        self.toggle_disabled_prompting(False)


    def record_voice_action(self):
        dlg = RecorderDialog(self.speechRecognizer)
        if dlg.exec():
            logging.info("Recorder Dialog Succeeded with transcription: " + dlg.trascription)
            self.promptbox.setText(dlg.trascription)

        
    def prompt_text_changed_action(self):
        isEmptyText = self.promptbox.toPlainText() == ""
        self.generateImageButton.setDisabled(isEmptyText)
        self.clearPrompt.setDisabled(isEmptyText)
