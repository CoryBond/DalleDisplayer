import logging
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import pyqtSignal, QRunnable, QThreadPool

from imageProviders.ImageProvider import ImageProvider, ImageProviderResult
from repoManager.Models import DeleteImagePrompsRequest
from repoManager.RepoManager import RepoManager, ImagePrompResult
from ui.dialogs.ErrorMessage import ErrorMessage
from ui.dialogs.LoadingPopup import LoadingPopup

from ui.widgets.home.ImageGenerator import ImageGenerator
from ui.widgets.home.ImageMeta import ImageMeta, ImageMetaInfo
from ui.widgets.home.ImageViewer import ImageViewer
from speechRecognition.SpeechRegonizer import SpeechRecognizer


class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)


def background_create_image_process(imageProvider: ImageProvider, prompt: str, loadSignal: pyqtSignal(str, object)):
    if(prompt is not None):
        response = imageProvider.get_image_from_string(prompt)

        loadSignal.emit(prompt, response)
    else:
        logging.warning("Prompt not provided!")


class HomePage(QSplitter):
    createImageSignal = pyqtSignal(str)
    loadNewImageSignal = pyqtSignal(str, dict)
    loadImageSignal = pyqtSignal(ImageMetaInfo, bytes)
    successfulSavedImageSignal = pyqtSignal()
    trashImageSignal = pyqtSignal()
    successfulTrashImageSignal = pyqtSignal()

    """
    QT Widget to generate and display AI images off of a prompt.
    Will load up the last generated image in PAIID.

    Attributes
    ----------

    Methods
    ----------

    """

    def __init__(self, repoManager: RepoManager, imageProvider : ImageProvider, speechRecognizer : SpeechRecognizer):
        super().__init__()

        self.repoManager = repoManager
        self.imageProvider = imageProvider

        self.threadpool = QThreadPool()
        # Pre-load common popups so there isn't a delay when they show up
        self.loadingScreen = LoadingPopup()

        self.createImageSignal.connect(self.create_image_action)
        self.loadNewImageSignal.connect(self.load_new_image_response)
        self.loadImageSignal.connect(self.load_image_response)
        self.trashImageSignal.connect(self.trash_image)

        loadResult = self.repoManager.get_latest_images_in_repo()
        self.init_ui(loadResult, speechRecognizer)


    def init_ui(self, lastImageResult: ImagePrompResult, speechRecognizer : SpeechRecognizer):
        self.imageGenerator = ImageGenerator(createImageSignal = self.createImageSignal, speechRecognizer = speechRecognizer)
        self.addWidget(self.imageGenerator)
        self.imageViewer = ImageViewer(lastImageResult.images[0] if lastImageResult is not None and len(lastImageResult.images) > 0 else None)
        self.addWidget(self.imageViewer)

        self.imageMetaInfo = ImageMetaInfo(
                prompt= lastImageResult.prompt, 
                date= lastImageResult.date, 
                time= lastImageResult.time, 
                engine= lastImageResult.repo,
                num= lastImageResult.num
            ) if lastImageResult is not None else None
        self.imageMeta = ImageMeta(self.trashImageSignal, self.imageMetaInfo)
        self.addWidget(self.imageMeta)
        self.setSizes([200, 800, 0])


    def load_new_image_response(self, prompt: str, response: ImageProviderResult):        
        if response['errorMessage'] != None:
            logging.info("error message  : " + response['errorMessage'])
            # Remove loading Screen so it doesn't overlap the error message
            self.loadingScreen.stop()
            ErrorMessage(response['errorMessage']).exec()
        else:
            saveResult = self.repoManager.save_image(prompt, response['img'])
            self.successfulSavedImageSignal.emit()

            self.imageViewer.replace_image(saveResult.images[0])
            self.imageMetaInfo = ImageMetaInfo(
                prompt= prompt,
                date= saveResult.date,
                time= saveResult.time,
                engine= saveResult.repo,
                num=str(saveResult.num)
            )
            self.imageMeta.loadMetaSignal.emit(self.imageMetaInfo)

        self.loadingScreen.stop()
        self.imageGenerator.toggle_disabled_prompting(False)


    def load_image_response(self, metaInfo: ImageMetaInfo, image):
        self.imageMetaInfo = metaInfo
        self.imageViewer.replace_image(image)
        self.imageMeta.loadMetaSignal.emit(metaInfo)


    def trash_image(self):
        result = self.repoManager.delete_image(DeleteImagePrompsRequest(
                prompt=self.imageMetaInfo.prompt,
                repo=self.imageMetaInfo.engine,
                date=self.imageMetaInfo.date,
                time=self.imageMetaInfo.time,
                nums=["1"]
            ))

        if result > 0:
            logging.info("Deleting successful")
            self.load_image_response(None, None)
            self.successfulTrashImageSignal.emit()
        else:
            logging.info("Deleting unsuccessful")


    def create_image_action(self, prompt: str):
        self.loadingScreen.showWithAnimation()

        imageGenerationProcess = ProcessRunnable(target=background_create_image_process, args=(self.imageProvider, prompt, self.loadNewImageSignal))
        self.threadpool.start(imageGenerationProcess)