
import logging
from pathlib import Path

import sys

sys.path.append(Path(__file__).parent.parent.as_posix()+"/src") # Add src directory to python path so we can access src modules
print(sys.path)

from depdencyInjection.Container import Container
from dependencyInjection.containerTestUtil import override_with_mock_image_provider

from utils.loggingUtils import configureBasicLogger


configureBasicLogger(filename="test_aiImageDisplayer.log", level=logging.DEBUG)


def main() -> None:
    """
    A developer UI that can be run rather then the main entry point from the source path.

    Will replace real API calling services with mock versions that simulate the behaviors the developer wants to see.
    """
    container = Container()
    override_with_mock_image_provider(container)

    container.uiOrchestrator().start()


if __name__ == "__main__":
    main()
