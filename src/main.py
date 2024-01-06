
from dependency_injector import containers, providers
import logging

from imageProviders.DalleProvider import DalleProvider
from ui.rootWindow import RootWindow
from utils.utils import get_project_root

logging.basicConfig()


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    dalleKeyFile = open(get_project_root()/".."/"dalle.key", "r")
    dalleKey = dalleKeyFile.read()
    dalleProvider = providers.Singleton(
        DalleProvider,
        key=dalleKey
    )

    ui = providers.Singleton(
        RootWindow,
        dalleProvider
    )


def main() -> None:
    container = Container()
    container.ui().start()


if __name__ == "__main__":
    main()
