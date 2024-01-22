
from depdencyInjection.Container import Container
from imageProviders.DalleProvider import ENGINE_NAME
from utils.loggingUtils import configureBasicLogger
from utils.pathingUtils import get_or_create_image_repos


configureBasicLogger()


def main() -> None:
    container = Container()
    container.config.repos.imageReposPath.from_value(get_or_create_image_repos())
    container.config.repos.startingRepo.from_value(ENGINE_NAME)

    container.uiOrchestrator().start()


if __name__ == "__main__":
    main()
