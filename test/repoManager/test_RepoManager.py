
from pathlib import Path
from utils.pathingUtils import DIRECTION

from depdencyInjection.Container import Container
from constantsTestUtil import TEST_RESOURCES_FOLDER_NAME, TEST_CONFIG
from repoManager.RepoManager import RepoManager
from repoManager.test_DirectoryIterator import populate_fs_with

from pyfakefs.fake_filesystem import FakeFilesystem 


TEST_RESOURCES_FOLDER_PATH = Path(TEST_RESOURCES_FOLDER_NAME)


def test_empty_fs_get_init_images(fs: FakeFilesystem):
   """
   Given emptry file system
   When get_init_images called
   Then return no results
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)
   repoManager: RepoManager = container.repoManager()

   # Act
   result = repoManager.get_init_images(2)
   
   # Assert
   assert result.results == [],  "result.results"
   assert result.nextToken is None, "result.nextToken"
   assert result.errorMessage is None, "result.errorMessage"


def test_images_exist_get_init_images(fs: FakeFilesystem):
   """
   Given single prompt entry
   When get_init_images for more then that called
   Then only the single entry returned
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)
   repoManager: RepoManager = container.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_PATH/"testRepo", fsState)

   # Act
   result = repoManager.get_init_images(2)
   
   # Assert
   assert len(result.results) == 1
   assert result.nextToken is None
   assert result.errorMessage is None

   [onlyResult] = result.results
   assert onlyResult.prompt == "Shrek Eat Chips"
   assert onlyResult.repo == "testRepo"
   assert onlyResult.date == "2024-01-14"
   assert onlyResult.time == "03:03:45.522668"
   assert onlyResult.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-14"/"03:03:45.522668_Shrek Eat Chips/1.png")]



def test_lots_of_images_exist_get_init_images(fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When get_init_images for less then that called
   Then entries requested returned
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)
   repoManager: RepoManager = container.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"],
         "01:03:45.522668_Donkey Eat Chips": ["1.png"]
      },
      "2024-01-13": { 
         "03:03:45.522668_Fiona Eat Chips": ["1.png"],
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_PATH/"testRepo", fsState)

   # Act
   result = repoManager.get_init_images(2)
   
   # Assert
   assert len(result.results) == 2
   assert result.nextToken is not None
   assert result.errorMessage is None

   [resultOne, resultTwo] = result.results
   assert resultOne.prompt == "Shrek Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-14"
   assert resultOne.time == "03:03:45.522668"
   assert resultOne.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-14"/"03:03:45.522668_Shrek Eat Chips/1.png")]

   assert resultTwo.prompt == "Donkey Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-14"
   assert resultTwo.time == "01:03:45.522668"
   assert resultTwo.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-14"/"01:03:45.522668_Donkey Eat Chips"/"1.png")]


def test_pagination(fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When subsequent calls to get_images with token provided
   Then result of the next page returned
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)
   repoManager: RepoManager = container.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"],
         "01:03:45.522668_Donkey Eat Chips": ["1.png"]
      },
      "2024-01-13": { 
         "03:03:45.522668_Fiona Eat Chips": ["1.png"],
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_PATH/"testRepo", fsState)

   # Act
   init_result = repoManager.get_init_images(2)
   result = repoManager.get_images(2, init_result.nextToken)

   # Assert
   assert len(result.results) == 1
   assert result.nextToken is None
   assert result.errorMessage is None

   [resultOne] = result.results
   assert resultOne.prompt == "Fiona Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-13"
   assert resultOne.time == "03:03:45.522668"
   assert resultOne.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-13"/"03:03:45.522668_Fiona Eat Chips/1.png")]


def test_backwards_pagination_normal(fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When subsequent calls to get_images with token provided (and backwards)
   Then result of the next page returned (sorted by most recent entries)
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)
   repoManager: RepoManager = container.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"],
         "01:03:45.522668_Donkey Eat Chips": ["1.png"]
      },
      "2024-01-13": { 
         "03:03:45.522668_Fiona Eat Chips": ["1.png"],
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_PATH/"testRepo", fsState)

   # Act
   init_result = repoManager.get_init_images(2)
   result = repoManager.get_images(2, init_result.nextToken, direction = DIRECTION.BACKWARD)

   # Assert
   [resultOne, resultTwo] = result.results
   assert resultOne.prompt == "Shrek Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-14"
   assert resultOne.time == "03:03:45.522668"
   assert resultOne.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-14"/"03:03:45.522668_Shrek Eat Chips/1.png")]

   assert resultTwo.prompt == "Donkey Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-14"
   assert resultTwo.time == "01:03:45.522668"
   assert resultTwo.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-14"/"01:03:45.522668_Donkey Eat Chips"/"1.png")]


def test_backwards_pagination_multi(fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When many subsequent calls to get_images with token provided (and backwards)
   Then result of the next page returned (sorted by most recent entries)
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)
   repoManager: RepoManager = container.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"],
         "01:03:45.522668_Donkey Eat Chips": ["1.png"]
      },
      "2024-01-13": { 
         "03:03:45.522668_Fiona Eat Chips": ["1.png"],
         "02:03:45.522668_Puss Eat Chips": ["1.png"],
         "01:03:45.522668_Farquaad Eat Chips": ["1.png"],
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_PATH/"testRepo", fsState)

   # Act
   init_result = repoManager.get_init_images(4)
   result1 = repoManager.get_images(2, init_result.nextToken, direction = DIRECTION.BACKWARD)
   result2 = repoManager.get_images(2, result1.nextToken, direction = DIRECTION.BACKWARD)

   # Assert
   assert len(result1.results) == 2

   [resultOne, resultTwo] = result1.results
   assert resultOne.prompt == "Fiona Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-13"
   assert resultOne.time == "03:03:45.522668"
   assert resultOne.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-13"/"03:03:45.522668_Fiona Eat Chips/1.png")]

   assert resultTwo.prompt == "Puss Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-13"
   assert resultTwo.time == "02:03:45.522668"
   assert resultTwo.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-13"/"02:03:45.522668_Puss Eat Chips/1.png")]

   assert len(result2.results) == 2
   assert result2.nextToken is None
   assert result2.errorMessage is None

   [resultOne, resultTwo] = result2.results
   assert resultOne.prompt == "Shrek Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-14"
   assert resultOne.time == "03:03:45.522668"
   assert resultOne.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-14"/"03:03:45.522668_Shrek Eat Chips/1.png")]

   assert resultTwo.prompt == "Donkey Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-14"
   assert resultTwo.time == "01:03:45.522668"
   assert resultTwo.pngPaths == [Path(TEST_RESOURCES_FOLDER_PATH/"testRepo"/"2024-01-14"/"01:03:45.522668_Donkey Eat Chips"/"1.png")]
