
import sys
from depdencyInjection.Container import Container
from utils.loggingUtils import configureBasicLogger
from PyQt5.QtWidgets import QApplication


configureBasicLogger()


def main() -> None:
    container = Container()
    container.ui().start()


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    main()
