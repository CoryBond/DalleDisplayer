"""
Test config file for all tests
"""
from typing import Union, Dict, List
import pytest
import os

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


TimeWithPromptDictType = Dict[str, List[str]]
DateDictType = Dict[str, TimeWithPromptDictType]


class FSHelpers:
    def __init__(self, fs: FakeFilesystem):
        self.fs = fs

    def populate_fs_with(self, path: Union[Path, str], dateDictStructure : DateDictType):
        """
        Simulates a files and folders in a fake file system when accessing the images repo.

        Will populate the fake file system with:

        * Dates folder
        * The TimePrompts of a date folder if the absolute date path is passed in
        * Images per TimePrompts
        """
        path = Path(path) # just in case the path provided is a string
        if(not os.path.exists(path)): # I know no other way with FakeFilesystem to first check if dirctory exists first.
            self.fs.create_dir(path) # Does not support  exist_ok=True flag like makedirs does :/
        for date, timePrompts in dateDictStructure.items():
            self.fs.create_dir(path/date)
            for timePrompt, images in timePrompts.items():
                self.fs.create_dir(directory_path=path/date/timePrompt)
                for image in images:
                    # Use a real image to simplify the test
                    self.fs.add_real_file(source_path=get_project_root()/'..'/'testResources'/'images'/'ai'/"test1.png", target_path=path/date/timePrompt/image)


@pytest.fixture
def fshelpers(fs: FakeFilesystem,):
    return FSHelpers(fs)


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
