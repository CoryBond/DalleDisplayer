import logging
from PyQt5.QtWidgets import QSplitter

from ui.widgets.home.ImageGenerator import ImageGenerator
from ui.widgets.home.ImageMeta import ImageMeta
from ui.widgets.home.ImageViewer import ImageViewer
from speechRecognition.SpeechRegonizer import SpeechRecognizer

class GalleryPage(QSplitter):
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

    def __init__(self, speechRecognizer : SpeechRecognizer):
        super().__init__()
