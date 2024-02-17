import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QLabel, QTextBrowser, QPushButton
from PyQt5.QtGui import QTextOption
from PyQt5.QtCore import pyqtSignal
from ui.widgets.common.QLine import QHLine

from utils.qtUtils import clear_layout


class ImageMetaInfo(object):
    def __init__(self, prompt: str, engine: str, date: str, time: str, num: str):
        self.prompt = prompt
        self.engine = engine
        self.date = date
        self.time = time
        self.num = num


DefaultImageMeta = ImageMetaInfo(prompt= '', date= '', time= '', engine= '', num= None)


class ImageMeta(QWidget):
    loadMetaSignal = pyqtSignal(object)

    """
    QT Widget to display image meta data.

    Attributes
    ----------
    loadMetaSignal
        signal to load meta contents to the ImageMeta widget

    Methods
    ----------

    """

    def __init__(self, trashImageSignal: pyqtSignal, initMetaInfo: ImageMetaInfo = DefaultImageMeta):
        super().__init__()

        self.trashImageSignal = trashImageSignal

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

        if(metaInfo is not None):
            # Replace layout contents with new meta info
            metaGroup = QGroupBox("Image Meta")
            metaLayout = QVBoxLayout()

            metaDetailLayout = QFormLayout()

            promptLabel = QTextBrowser() # QTextBrowser better supports word wrap when words are so big they need to arbitrarily be cut across lines
            promptLabel.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
            promptLabel.setText(metaInfo.prompt)
            metaDetailLayout.addRow(QLabel("Prompt: "), promptLabel)
            metaDetailLayout.addRow(QLabel("Date: "), QLabel(metaInfo.date))
            metaDetailLayout.addRow(QLabel("Time: "), QLabel(metaInfo.time))
            metaDetailLayout.addRow(QLabel("Engine: "), QLabel(metaInfo.engine))
            metaDetailLayout.addRow(QLabel("Num: "), QLabel(metaInfo.num))

            metaLayout.addLayout(metaDetailLayout)

            metaGroup.setLayout(metaLayout)
            self.layout().addWidget(metaGroup)
        
            self.layout().addWidget(QHLine())

            self.trashImageButton = QPushButton('Trash Image', self)
            self.trashImageButton.setStyleSheet("background-color: red")
            self.trashImageButton.clicked.connect(lambda : self.trashImageSignal.emit())
            self.layout().addWidget(self.trashImageButton)
