from dependency_injector import containers, providers
from imageProviders.DalleProvider import DalleProvider
from repoManager.RepoManager import RepoManager
from speechRecognition.GoogleSpeachRecognizer import GoogleSpeechRecognizer
from ui.widgets.MainWindow import MainWindow
from ui.QApplicationManager import QApplicationManager
from ui.UIOrchestrator import UIOrchestrator
from ui.widgets.home.HomePage import HomePage
from ui.widgets.gallery.GalleryPage import GalleryPage

from utils.pathingUtils import get_project_root

from utils.pageUtils import PageDictType, PageName, PageCaption, PageHint, PageMetaDecorator


class PagesDispatcher:
    pages: PageDictType


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

    home = providers.Singleton(HomePage, repoManager, imageProvider, speechRecognizer),
    gallery = providers.Singleton(GalleryPage, repoManager),

    homePageMeta = providers.Singleton(PageMetaDecorator, home[0], PageName.HOME, PageCaption.HOME, PageHint.HOME),
    galleryPageMeta = providers.Singleton(PageMetaDecorator, gallery[0], PageName.GALLERY, PageCaption.GALLERY, PageHint.GALLERY),

    mainWindow = providers.Singleton(
        MainWindow,
        homePageMeta[0],
        galleryPageMeta[0]
    )

    uiOrchestrator = providers.Singleton(
        UIOrchestrator,
        qApplicationManager,
        home[0],
        gallery[0],
        mainWindow
    )