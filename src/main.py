
from depdencyInjection.Container import Container
from utils.loggingUtils import configureBasicLogger


configureBasicLogger()


def main() -> None:
    container = Container()
    container.uiOrchestrator().start()


if __name__ == "__main__":
    main()
