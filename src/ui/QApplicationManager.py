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
            

# Custom styling 
customstyling = """
QWidget { 
    font-size: 14pt;
}

QPushButton {
    height: 40px;
}
"""


class QApplicationManager(object):


    def __init__(self):
        os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
        self.app = QApplication(sys.argv)
        QGuiApplication.inputMethod().visibleChanged.connect(handleVisibleChanged)

        self.applyStyling()

        return


    def applyStyling(self):
        # final style sheet
        styleSheet = qdarkstyle.load_stylesheet_pyqt5() + customstyling
        self.app.setStyleSheet(styleSheet)
       

    def getQApp(self):
        return self.app