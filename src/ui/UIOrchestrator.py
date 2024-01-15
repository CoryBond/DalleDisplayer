
import logging
import sys

from ui.widgets.MainWindow import MainWindow
from ui.QApplicationManager import QApplicationManager


class QtBot():
    """
    Interface for a QT bot that runs alongside QT sending events, manipulating the QT runtime or doing other things that are required
    when QT is running.

    Very useful for testing purposes when a Bot can help deconstruct widgets or send test events.
    """
    def addWidget(self, widget, *, before_close_func=None):
        return


class UIOrchestrator():
    """
    Orchestrator class that takes all high level QT resources, combines them together and generally controls how they are used.

    Attributes
    ----------

    Methods
    ----------
    start()
        Runs the PAIID application UI. Will close the current python interpreter after the UI application runs or at least failed to run.

    start_with_bot(qtbot)
        Runs the PAIID application UI on the current thread but with a QTbot running alongside it.
        Does not close the python interpreter.
    """

    def __init__(self, qApplicationManager: QApplicationManager, mainWindow: MainWindow):
        self.app = qApplicationManager.getQApp()
        self.mainWindow = mainWindow
        return


    def start(self):
        logging.info("Starting UI")

        self.mainWindow.show()
        sys.exit(self.app.exec_())


    def start_with_bot(self, qtbot: QtBot):
        logging.info("Starting UI with bot")

        qtbot.addWidget(self.mainWindow)
        self.mainWindow.show()
