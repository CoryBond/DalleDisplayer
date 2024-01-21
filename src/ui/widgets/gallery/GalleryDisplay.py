
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

from typing import List

from repoManager.RepoManager import ImagePrompResult
from ui.widgets.common.QLine import QHLine
from utils.qtUtils import clear_layout


class ImagesDisplay(QWidget):

    imageClicked = pyqtSignal([str])  # Signal emited when image is clicked

    def __init__(self, image: ImagePrompResult):
        super().__init__()

        self.init_ui(image)


    def init_ui(self, image: ImagePrompResult):

        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        layout.addLayout(self.create_header(image))

        layout.addWidget(QHLine())

        layout.addWidget(self.create_image(image.pngPaths[0]))

        self.setLayout(layout)


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
    

    def create_image(self, imgPath: Path) -> QLabel:
        pixmap = QPixmap(imgPath.as_posix())
        label = QLabel()
        label.resize(75, 75)
        label.setPixmap(pixmap.scaled(label.size(), Qt.IgnoreAspectRatio))
        return label


class GalleryDisplay(QScrollArea):


    def __init__(self, images: List[ImagePrompResult] = []):
        super().__init__()

        self.init_ui(images)


    def init_ui(self, images: List[ImagePrompResult] = []):
        self.replace_display(images)


    def replace_display(self, images: List[ImagePrompResult]):
        # First remove widget
        self.takeWidget()
        # Add in new widget
        self.setWidget(self.create_scrollable_widget(images))


    def create_scrollable_widget(self, images: List[ImagePrompResult]):
        layout = QVBoxLayout()

        for image in images:
            layout.addWidget(ImagesDisplay(image))

        childWidget = QWidget()
        childWidget.setLayout(layout)
        return childWidget