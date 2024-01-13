
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
    container = Container()
    override_with_mock_image_provider(container)

    container.uiOrchestrator().start()


if __name__ == "__main__":
    main()
