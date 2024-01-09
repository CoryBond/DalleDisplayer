
import os
import sys
from dependency_injector import containers, providers
from imageProviders.DalleProvider import DalleProvider
from ui.MainWindow import MainWindow
from ui.UIApplication import UIApplication
from utils.pathingUtils import get_project_root
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication, QRegion

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

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    dalleKeyFile = open(get_project_root()/".."/"dalle.key", "r")
    dalleKey = dalleKeyFile.read()
    imageProvider = providers.Singleton(
        DalleProvider,
        key=dalleKey
    )

    # Must always be made first in the QT framework! If not made first other QTWidgets will error.
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    app = providers.Singleton(
        QApplication,
        sys.argv
    )
    # QGuiApplication.inputMethod().visibleChanged.connect(handleVisibleChanged)

    mainWindow = providers.Singleton(
        MainWindow,
        imageProvider
    )

    ui = providers.Singleton(
        UIApplication,
        app,
        mainWindow
    )