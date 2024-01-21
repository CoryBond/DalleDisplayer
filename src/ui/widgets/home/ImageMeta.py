import logging
from typing import TypedDict
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QLabel
from PyQt5.QtCore import pyqtSignal

from utils.qtUtils import clear_layout


class ImageMetaInfo(object):
    def __init__(self, prompt: str, engine: str, date: str, time: str, num: int):
        self.prompt = prompt
        self.engine = engine
        self.date = date
        self.time = time
        self.num = num


DefaultImageMeta = ImageMetaInfo(prompt= '', date= '', time= '', engine= '', num= None)


class ImageMeta(QWidget):
    loadMetaSignal = pyqtSignal(object)

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

    def __init__(self, initMetaInfo: ImageMetaInfo = DefaultImageMeta):
        super().__init__()

        self.setGeometry(100, 100, 300, 400)

        self.loadMetaSignal.connect(self.replace_meta)

        self.init_ui(initMetaInfo)


    def init_ui(self, initMetaInfo: ImageMetaInfo):
        # Make the layout
        self.setLayout(QVBoxLayout())

        # Before adding its contents
        self.loadMetaSignal.emit(initMetaInfo)


    def replace_meta(self, metaInfo: ImageMetaInfo):
        # clear the existing layout
        clear_layout(layout=self.layout())

        print("metaInfo")
        print(str(metaInfo))

        # Replace layout contents with new meta info
        metaGroup = QGroupBox("Image Meta")
        metaLayout = QVBoxLayout()

        metaDetailLayout = QFormLayout()

        metaDetailLayout.addRow(QLabel("Prompt: "), QLabel(metaInfo.prompt))
        metaDetailLayout.addRow(QLabel("Date: "), QLabel(metaInfo.date))
        metaDetailLayout.addRow(QLabel("Time: "), QLabel(metaInfo.time))
        metaDetailLayout.addRow(QLabel("Engine: "), QLabel(metaInfo.engine))
        metaDetailLayout.addRow(QLabel("Num: "), QLabel(metaInfo.num))

        metaLayout.addLayout(metaDetailLayout)

        metaGroup.setLayout(metaLayout)
        self.layout().addWidget(metaGroup)
        
