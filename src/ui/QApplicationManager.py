import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QGuiApplication, QRegion
import qdarkstyle


# From the answers at https://stackoverflow.com/questions/63955568/how-to-find-the-window-that-contains-the-qtvirtualkeyboard
# To solve virtual keyboard overlapping with the application
def handleVisibleChanged():
    if not QGuiApplication.inputMethod().isVisible():
        return
    for w in QGuiApplication.allWindows():
        if w.metaObject().className() == "QtVirtualKeyboard::InputView":
            keyboard = w.findChild(QObject, "keyboard")
            if keyboard is not None:
                r = w.geometry()
                r.moveTop(keyboard.property("y"))
                w.setMask(QRegion(r))
                return

ghost_white = "#f8f8ff"

# Dark Mode Patching
darkmodepatchedstyle = """
QHLine#PAIID_QHLine { 
    border: 2px solid #f8f8ff;
}

"""


# Custom styling 
customstyling = """
QWidget { 
    font-size: 14pt;
}

QPushButton {
    height: 40px;
}

QSplitter {
    width: 25px;
}

QScrollBar:vertical {
    width: 25px;
 } 

"""


class QApplicationManager(object):
    """
    Wrapper class which manages a QApplication instance. 
    
    For any QT project a QApplication object MUST be created before any other widgets. Additionally for some QT features, like plugins, some programmatic registration and setup
    is required before an QApplications can be made. This manager handles all of that within its constructor.

    Some settings/features this manager applies at construction time include:
    1. Dark mode theming
    2. Setup the QT Virtual Keyboard

    Future versions of this manager can also allow dynamic manipulcation of the QApplication after construction time (for example, switching themes for the entire application.)

    Attributes
    ----------

    Methods
    ----------
    applyStyling()
        Applies application wide styling. This includes darkmode and styles to make text/widgets bigger for a smaller screen.

    getQApp()
        Gets the singleton QApplication object
    """

    def __init__(self):
        os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
        self.app = QApplication(sys.argv)
        QGuiApplication.inputMethod().visibleChanged.connect(handleVisibleChanged)

        self.applyStyling()

        return


    def applyStyling(self) -> None:
        # final style sheet
        styleSheet = qdarkstyle.load_stylesheet_pyqt5() + darkmodepatchedstyle + customstyling
        self.app.setStyleSheet(styleSheet)


    def getQApp(self) -> QApplication:
        return self.app