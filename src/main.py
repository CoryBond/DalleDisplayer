
from dependency_injector import containers, providers
from imageProviders.DalleProvider import DalleProvider

from ui.rootWindow import RootWindow


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    dalle_provider = providers.Singleton(
        DalleProvider,
        key=""
    )

    ui = providers.Singleton(
        RootWindow
    )


def main() -> None:
    container = Container()
    container.ui().start()


if __name__ == "__main__":
    main()
