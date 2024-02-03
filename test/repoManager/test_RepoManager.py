
from pathlib import Path
from utils.pathingUtils import DIRECTION

from PIL import Image
from io import BytesIO

from depdencyInjection.Container import Container
from repoManager.RepoManager import RepoManager
from repoManager.test_DirectoryIterator import populate_fs_with

from pyfakefs.fake_filesystem import FakeFilesystem 


def test_empty_fs_get_images(containerWithMocks: Container):
   """
   Given emptry file system
   When get_images called
   Then return no results
   """

   # Arrange
   repoManager: RepoManager = containerWithMocks.repoManager()

   # Act
   result = repoManager.get_images(2)
   
   # Assert
   assert result.results == [],  "result.results"
   assert result.nextToken is None, "result.nextToken"
   assert result.errorMessage is None, "result.errorMessage"


def test_images_exist_get_images(containerWithMocks: Container, fs: FakeFilesystem):
   """
   Given single prompt entry
   When get_images for more then that called
   Then only the single entry returned
   """

   # Arrange
   repoManager: RepoManager = containerWithMocks.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)

   # Act
   result = repoManager.get_images(2)
   
   # Assert
   assert len(result.results) == 1
   assert result.nextToken is None
   assert result.errorMessage is None

   [onlyResult] = result.results
   assert onlyResult.prompt == "Shrek Eat Chips"
   assert onlyResult.repo == "testRepo"
   assert onlyResult.date == "2024-01-14"
   assert onlyResult.time == "03:03:45.522668"
   Image.open(onlyResult.images[0]) # if no exception is thrown then the bytes are a proper image



def test_lots_of_images_exist_get_images(containerWithMocks: Container, fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When get_images for less then that called
   Then entries requested returned
   """

   # Arrange
   repoManager: RepoManager = containerWithMocks.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"],
         "01:03:45.522668_Donkey Eat Chips": ["1.png"]
      },
      "2024-01-13": { 
         "03:03:45.522668_Fiona Eat Chips": ["1.png"],
      }
   }
   populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)

   # Act
   result = repoManager.get_images(2)
   
   # Assert
   assert len(result.results) == 2
   assert result.nextToken is not None
   assert result.errorMessage is None

   [resultOne, resultTwo] = result.results
   assert resultOne.prompt == "Shrek Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-14"
   assert resultOne.time == "03:03:45.522668"
   Image.open(resultOne.images[0]) # if no exception is thrown then the bytes are a proper image

   assert resultTwo.prompt == "Donkey Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-14"
   assert resultTwo.time == "01:03:45.522668"
   Image.open(resultTwo.images[0]) # if no exception is thrown then the bytes are a proper image


def test_pagination(containerWithMocks: Container, fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When subsequent calls to get_images with token provided
   Then result of the next page returned
   """

   # Arrange
   repoManager: RepoManager = containerWithMocks.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"],
         "01:03:45.522668_Donkey Eat Chips": ["1.png"]
      },
      "2024-01-13": { 
         "03:03:45.522668_Fiona Eat Chips": ["1.png"],
      }
   }
   populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)

   # Act
   init_result = repoManager.get_images(2)
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
   Image.open(resultOne.images[0]) # if no exception is thrown then the bytes are a proper image


def test_backwards_pagination_normal(containerWithMocks: Container, fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When subsequent calls to get_images with token provided (and backwards)
   Then result of the next page returned (sorted by most recent entries)
   """

   # Arrange
   repoManager: RepoManager = containerWithMocks.repoManager()

   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"],
         "01:03:45.522668_Donkey Eat Chips": ["1.png"]
      },
      "2024-01-13": { 
         "03:03:45.522668_Fiona Eat Chips": ["1.png"],
      }
   }
   populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)

   # Act
   init_result = repoManager.get_images(2)
   result = repoManager.get_images(2, init_result.nextToken, direction = DIRECTION.BACKWARD)

   # Assert
   [resultOne, resultTwo] = result.results
   assert resultOne.prompt == "Shrek Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-14"
   assert resultOne.time == "03:03:45.522668"
   Image.open(resultOne.images[0]) # if no exception is thrown then the bytes are a proper image

   assert resultTwo.prompt == "Donkey Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-14"
   assert resultTwo.time == "01:03:45.522668"
   Image.open(resultTwo.images[0]) # if no exception is thrown then the bytes are a proper image


def test_backwards_pagination_multi(containerWithMocks: Container, fs: FakeFilesystem):
   """
   Given lots of prompt entries
   When many subsequent calls to get_images with token provided (and backwards)
   Then result of the next page returned (sorted by most recent entries)
   """

   # Arrange
   repoManager: RepoManager = containerWithMocks.repoManager()

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
   populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)

   # Act
   init_result = repoManager.get_images(4)
   result1 = repoManager.get_images(2, init_result.nextToken, direction = DIRECTION.BACKWARD)
   result2 = repoManager.get_images(2, result1.nextToken, direction = DIRECTION.BACKWARD)

   # Assert
   assert len(result1.results) == 2

   [resultOne, resultTwo] = result1.results
   assert resultOne.prompt == "Fiona Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-13"
   assert resultOne.time == "03:03:45.522668"
   Image.open(resultOne.images[0]) # if no exception is thrown then the bytes are a proper image

   assert resultTwo.prompt == "Puss Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-13"
   assert resultTwo.time == "02:03:45.522668"
   Image.open(resultTwo.images[0]) # if no exception is thrown then the bytes are a proper image

   assert len(result2.results) == 2
   assert result2.nextToken is None
   assert result2.errorMessage is None

   [resultOne, resultTwo] = result2.results
   assert resultOne.prompt == "Shrek Eat Chips"
   assert resultOne.repo == "testRepo"
   assert resultOne.date == "2024-01-14"
   assert resultOne.time == "03:03:45.522668"
   Image.open(resultOne.images[0]) # if no exception is thrown then the bytes are a proper image

   assert resultTwo.prompt == "Donkey Eat Chips"
   assert resultTwo.repo == "testRepo"
   assert resultTwo.date == "2024-01-14"
   assert resultTwo.time == "01:03:45.522668"
   Image.open(resultTwo.images[0]) # if no exception is thrown then the bytes are a proper image
