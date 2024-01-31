
import logging
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage

from typing import List

from repoManager.RepoManager import ImagePrompResult
from ui.widgets.common.QLine import QHLine
from ui.widgets.home.ImageMeta import ImageMetaInfo


class ImagesDisplay(QWidget):
    imageClickedSignal =  pyqtSignal(ImageMetaInfo, QImage)

    def __init__(self, image: ImagePrompResult):
        super().__init__()

        self.init_ui(image)


    def init_ui(self, image: ImagePrompResult):

        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        layout.addLayout(self.create_header(image))

        layout.addWidget(QHLine())

        self.image_label = self.create_image(image, image.pngPaths[0])
        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.image_meta = image


    def create_header(self, image: ImagePrompResult) -> QVBoxLayout:
        headerLayout = QVBoxLayout()
        headerLayout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        headerLayout.addWidget(QLabel(image.prompt))

        subInfoLayout = QHBoxLayout()
        subInfoLayout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        subInfoLayout.addWidget(QLabel("Time:"))
        subInfoLayout.addWidget(QLabel(image.time))
        subInfoLayout.addWidget(QLabel("Date:"))
        subInfoLayout.addWidget(QLabel(image.date))

        headerLayout.addLayout(subInfoLayout)
        return headerLayout
    

    def create_image(self, image: ImagePrompResult, imgPath: Path) -> QLabel:
        pixmap = QPixmap(imgPath.as_posix())
        label = QLabel()
        label.resize(75, 75)
        label.setPixmap(pixmap.scaled(label.size(), Qt.IgnoreAspectRatio))
        def leftClickEvent(event):
            if event.button() == Qt.LeftButton:
                self.imageClickedSignal.emit(
                    ImageMetaInfo(
                        prompt=image.prompt, date=image.date, time=image.time, engine=image.repo, num="1"
                    ), 
                    pixmap.toImage()
                )
        label.mousePressEvent = leftClickEvent
        return label


class GalleryDisplay(QScrollArea):
    imageClickedSignal = pyqtSignal(ImageMetaInfo, QImage)


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


    def create_scrollable_widget(self, images: List[ImagePrompResult]):
        layout = QVBoxLayout()

        logging.debug(f'Recieving {len(images)} images')

        for image in images:
            imageDisplay = ImagesDisplay(image)
            imageDisplay.imageClickedSignal.connect(self.imageClickedSignal.emit)
            layout.addWidget(imageDisplay)

        childWidget = QWidget()
        childWidget.setLayout(layout)
        return childWidget