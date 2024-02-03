"""
Test config file for all tests
"""
import pytest

import time
from pathlib import Path
from unittest.mock import patch                                       
from depdencyInjection.Container import Container
from imageProviders.ImageProvider import ImageProvider, ImageProviderResult

from utils.pathingUtils import get_project_root, get_or_create_resources, read_file_as_bytes
from pyfakefs.fake_filesystem import FakeFilesystem 


TEST_RESOURCES_FOLDER_NAME = "testResources"

TEST_RESOURCES_FOLDER_PATH = Path(TEST_RESOURCES_FOLDER_NAME)

TEST_RESOURCES = get_or_create_resources(TEST_RESOURCES_FOLDER_NAME)

TEST_CONFIG = TEST_RESOURCES/"configs"/"test_config.yml"


def test_image_generator():
        """
        Simulates a image getting generting by loading an existing image from the testResources folder.
        Will also simulate "lag" by sleeping the current thread.
        Should be run in a seperate thread as to prevent UI event loop from being freezed as well.
        """
        TestFile1 = read_file_as_bytes(get_project_root()/'..'/'testResources'/'images'/'ai'/"test1.png")
        TestFile2 = read_file_as_bytes(get_project_root()/'..'/'testResources'/'images'/'ai'/"test2.png")
        i = 0
        def cb(prompt: str) -> ImageProviderResult:
            nonlocal i 
            i += 1
            time.sleep(4)
            img = TestFile1 if i % 2 == 0 else TestFile2
            return { 'img': img, 'errorMessage': None }
        return cb


@patch('imageProviders.ImageProvider')
def override_with_mock_image_provider(container: Container, imageProvider: ImageProvider):
    """
    Creates a generic mock of ImageProvider and adds it to the dependency injection container
    """
    imageProvider.engine_name = lambda : "mockGenerator"
    imageProvider.get_image_from_string = test_image_generator()

    container.imageProvider.override(imageProvider)


@pytest.fixture
def containerWithMocks(fs: FakeFilesystem):
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)

   # Override with fake image provider.... temp turn of fs so we can access files for the
   # image provider to use 
   fs.pause()
   override_with_mock_image_provider(container)
   fs.resume()
   return container