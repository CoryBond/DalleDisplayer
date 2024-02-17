
import logging
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

from typing import List

from repoManager.RepoManager import ImagePrompResult
from ui.widgets.common.QLine import QHLine
from ui.widgets.home.ImageMeta import ImageMetaInfo


class ImagesDisplay(QWidget):
    """
    QT Widget to display a singular image prompt.
    This inculdes meta data of the image prompt like date, time, images generated and prompt used.

    Attributes
    ----------
    imageClickedSignal
        signal that is emited when the image is clicked in the gallery

    Methods
    ----------
    """
    imageClickedSignal =  pyqtSignal(ImageMetaInfo, bytes)

    def __init__(self, imageResult: ImagePrompResult):
        super().__init__()

        self.init_ui(imageResult)


    def init_ui(self, imageResult: ImagePrompResult):

        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        layout.addLayout(self.create_header(imageResult))

        layout.addWidget(QHLine())

        for image in imageResult.images:
            self.image_label = self.create_image(imageResult, image)
            layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.image_meta = imageResult


    def create_header(self, imageResult: ImagePrompResult) -> QVBoxLayout:
        headerLayout = QVBoxLayout()
        headerLayout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        headerLayout.addWidget(QLabel(imageResult.prompt))

        subInfoLayout = QHBoxLayout()
        subInfoLayout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        subInfoLayout.addWidget(QLabel("Time:"))
        subInfoLayout.addWidget(QLabel(imageResult.time))
        subInfoLayout.addWidget(QLabel("Date:"))
        subInfoLayout.addWidget(QLabel(imageResult.date))

        headerLayout.addLayout(subInfoLayout)
        return headerLayout
    

    def create_image(self, imageResult: ImagePrompResult, imageBytes: bytes) -> QLabel:
        pixmap = QPixmap()
        pixmap.loadFromData(imageBytes)
        label = QLabel()
        label.resize(75, 75)
        label.setPixmap(pixmap.scaled(label.size(), Qt.IgnoreAspectRatio))
        def leftClickEvent(event):
            if event.button() == Qt.LeftButton:
                self.imageClickedSignal.emit(
                    ImageMetaInfo(
                        prompt=imageResult.prompt, date=imageResult.date, time=imageResult.time, engine=imageResult.repo, num="1"
                    ), 
                    imageBytes
                )
        label.mousePressEvent = leftClickEvent
        return label


class GalleryDisplay(QScrollArea):
    """
    QT Widget to display a single page worth of image prompts.

    Attributes
    ----------
    imageClickedSignal
        signal that is emited when any image is clicked in the gallery

    Methods
    ----------
    replace_display()
        Replaces the page with a new page worth of image prompts
    """
    imageClickedSignal = pyqtSignal(ImageMetaInfo, object)


    def __init__(self, images: List[ImagePrompResult] = []):
        super().__init__()

        self.init_ui(images)


    def init_ui(self, images: List[ImagePrompResult] = []):
        self.replace_display(images)


    def replace_display(self, images: List[ImagePrompResult]):
        # First remove widget
        self.takeWidget()
        # Add in new widget
        self.contentWidget = self.create_scrollable_widget(images)
        self.setWidget( self.contentWidget)


    def create_scrollable_widget(self, imageResults: List[ImagePrompResult]):
        layout = QVBoxLayout()

        logging.debug(f'Recieving {len(imageResults)} images')

        for imageResult in imageResults:
            imageDisplay = ImagesDisplay(imageResult)
            imageDisplay.imageClickedSignal.connect(self.imageClickedSignal.emit)
            layout.addWidget(imageDisplay)

        childWidget = QWidget()
        childWidget.setLayout(layout)
        return childWidget