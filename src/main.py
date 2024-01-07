
import logging

from depdencyInjection.Container import Container


logging.basicConfig()


def main() -> None:
    container = Container()
    container.ui().start()


if __name__ == "__main__":
    main()
