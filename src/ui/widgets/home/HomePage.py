import logging
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import pyqtSignal, QRunnable, QThreadPool

from imageProviders.ImageProvider import ImageProvider, ImageProviderResult
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
    loadNewImageSignal = pyqtSignal(str, object)
    loadImageSignal = pyqtSignal(ImageMetaInfo, object)
    saveImageSignal = pyqtSignal()

    """
    QT Widget to display a singular and move a singular image.
    
    Images can be moved via:
    1. Panning the image when click/touch drag movements
    2. Zomming in/out of the image with a pinch (touch) gesture anywhere in the viewer

    Attributes
    ----------

    Methods
    ----------
    replace_image(imagePath)
        Replaces the current image with a new one from the given path. The new image will "fit" into the views current frame when fully loaded.

    has_photo()
        Returns if the current view has any image loaded to it currently
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

        loadResult = self.repoManager.get_latest_images_in_repo()
        self.init_ui(loadResult, speechRecognizer)


    def init_ui(self, lastImageResult: ImagePrompResult, speechRecognizer : SpeechRecognizer):
        self.imageGenerator = ImageGenerator(createImageSignal = self.createImageSignal, speechRecognizer = speechRecognizer)
        self.addWidget(self.imageGenerator)
        self.imageViewer = ImageViewer(lastImageResult.pngPaths[0] if lastImageResult is not None and len(lastImageResult.pngPaths) > 0 else None)
        self.addWidget(self.imageViewer)
        self.imageMeta = ImageMeta(ImageMetaInfo(
                prompt= lastImageResult.prompt, 
                date= lastImageResult.date, 
                time= lastImageResult.time, 
                engine= lastImageResult.repo,
                num= lastImageResult.num
            ) if lastImageResult is not None else None)
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
            self.saveImageSignal.emit()

            self.imageViewer.replace_image(saveResult.pngPaths[0].as_posix())
            self.imageMeta.loadMetaSignal.emit(ImageMetaInfo(
                prompt= prompt,
                date= saveResult.date,
                time= saveResult.time,
                engine= saveResult.repo,
                num=str(saveResult.num)
            ))

        self.loadingScreen.stop()
        self.imageGenerator.toggle_disabled_prompting(False)


    def load_image_response(self, metaInfo: ImageMetaInfo, image):        
        self.imageViewer.replace_image(image)
        self.imageMeta.loadMetaSignal.emit(metaInfo)


    def create_image_action(self, prompt: str):
        self.loadingScreen.showWithAnimation()

        imageGenerationProcess = ProcessRunnable(target=background_create_image_process, args=(self.imageProvider, prompt, self.loadNewImageSignal))
        self.threadpool.start(imageGenerationProcess)