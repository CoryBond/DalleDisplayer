from dependency_injector import containers, providers
from imageProviders.DalleProvider import DalleProvider
from repoManager.RepoManager import RepoManager
from speechRecognition.GoogleSpeachRecognizer import GoogleSpeechRecognizer
from ui.widgets.MainWindow import MainWindow
from ui.QApplicationManager import QApplicationManager
from ui.UIOrchestrator import UIOrchestrator
from utils.pathingUtils import get_project_root


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    dalleKeyFile = open(get_project_root()/".."/"dalle.key", "r")
    dalleKey = dalleKeyFile.read()
    imageProvider = providers.Singleton(
        DalleProvider,
        key=dalleKey
    )

    qApplicationManager = providers.Singleton(
        QApplicationManager
    )

    speechRecognizer = providers.Singleton(
        GoogleSpeechRecognizer
    )

    repoManager = providers.Singleton(
        RepoManager,
        imageProvider.provided.engine_name.call(),
    )

    mainWindow = providers.Singleton(
        MainWindow,
        imageProvider,
        repoManager,
        speechRecognizer
    )

    uiOrchestrator = providers.Singleton(
        UIOrchestrator,
        qApplicationManager,
        mainWindow
    )