from pathlib import Path
from utils.pathingUtils import get_or_create_resources


TEST_RESOURCES_FOLDER_NAME = "testResources"

TEST_RESOURCES_FOLDER_PATH = Path(TEST_RESOURCES_FOLDER_NAME)

TEST_RESOURCES = get_or_create_resources(TEST_RESOURCES_FOLDER_NAME)

TEST_CONFIG = TEST_RESOURCES/"configs"/"test_config.yml"
