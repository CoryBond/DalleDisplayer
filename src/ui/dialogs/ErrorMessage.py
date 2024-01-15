from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt


class ErrorMessage(QMessageBox):
    """
    Simple error message when AI image generation fails

    Attributes
    ----------

    Methods
    ----------
    """

    def __init__(self, message: str):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Error While Generating Image!")
        self.setText(message)
        self.setStandardButtons(QMessageBox.Close)
        self.setIcon(QMessageBox.Critical)
