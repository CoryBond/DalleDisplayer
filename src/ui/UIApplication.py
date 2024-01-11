
import logging
import sys

from ui.widgets.MainWindow import MainWindow
from ui.QApplicationManager import QApplicationManager


class UIApplication():


    def __init__(self, qApplicationManager: QApplicationManager, mainWindow: MainWindow):
        self.app = qApplicationManager.getQApp()
        self.mainWindow = mainWindow
        return


    def start(self):
        logging.info("Starting UI")

        self.mainWindow.show()
        sys.exit(self.app.exec_())