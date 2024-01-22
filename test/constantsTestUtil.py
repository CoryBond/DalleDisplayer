from utils.pathingUtils import get_or_create_resources


TEST_RESOURCES_FOLDER_NAME = "testResources"
TEST_RESOURCES = get_or_create_resources(TEST_RESOURCES_FOLDER_NAME)
TEST_CONFIG = TEST_RESOURCES/"configs"/"test_config.yml"
