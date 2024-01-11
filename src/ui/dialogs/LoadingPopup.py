import logging
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie

from utils.pathingUtils import get_or_create_image_resources


class LoadingPopup(QDialog):


    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.layout = QVBoxLayout()

        self.movie = QMovie((get_or_create_image_resources()/"medium_cat_loading.gif").as_posix())
        self.animation = QLabel(self)
        self.animation.setMovie(self.movie)

        self.layout.addWidget(self.animation)

        self.setLayout(self.layout)


    def showWithAnimation(self):
        self.movie.start()
        self.show()

    def stop(self):
        self.movie.stop()
        self.close()