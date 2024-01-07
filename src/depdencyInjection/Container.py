
from dependency_injector import containers, providers
from imageProviders.DalleProvider import DalleProvider
from ui.rootWindow import RootWindow
from utils.utils import get_project_root

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    dalleKeyFile = open(get_project_root()/".."/"dalle.key", "r")
    dalleKey = dalleKeyFile.read()
    imageProvider = providers.Singleton(
        DalleProvider,
        key=dalleKey
    )

    ui = providers.Singleton(
        RootWindow,
        imageProvider
    )