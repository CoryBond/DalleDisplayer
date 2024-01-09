
import logging
from tkinter import *
from PIL import ImageTk
import os

from imageProviders.ImageProvider import ImageProvider
from ui.MainWindow import MainWindow

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

class UIApplication():


    def __init__(self, app, mainWindow):
        self.app = app
        self.mainWindow = mainWindow
        return
    

    def start(self):
        logging.info("Starting UI")


        self.mainWindow.show()
        sys.exit(self.app.exec_())