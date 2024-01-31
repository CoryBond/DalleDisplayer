import os
from pathlib import Path
from typing import Dict, List, Union

import pytest

from constantsTestUtil import TEST_RESOURCES_FOLDER_NAME
from repoManager.DirectoryIterator import DirectoryIterator

from utils.pathingUtils import DIRECTION

from pyfakefs.fake_filesystem import FakeFilesystem 


TimeWithPromptDictType = Dict[str, List[str]]
DateDictType = Dict[str, TimeWithPromptDictType]


def populate_fs_with(fs: FakeFilesystem, path: Union[Path, str], dateDictStructure : DateDictType):
   """
   Simulates a files and folders in a fake file system when accessing the images repo.

   Will populate the fake file system with:

   * Dates folder
   * The TimePrompts of a date folder if the absolute date path is passed in
   * Images per TimePrompts
   """
   path = Path(path) # just in case the path provided is a string
   if(not os.path.exists(path)): # I know no other way with FakeFilesystem to first check if dirctory exists first.
      fs.create_dir(path) # Does not support  exist_ok=True flag like makedirs does :/
   for date, timePrompts in dateDictStructure.items():
      fs.create_dir(path/date)
      for timePrompt, images in timePrompts.items():
         fs.create_dir(path/date/timePrompt)
         for image in images:
            fs.create_file(path/date/timePrompt/image)


def test_exception_thrown_on_existant_directory(fs: FakeFilesystem):
   """
   Given non-existent path to directories 
   When DirectoryIterator created
   Then exception of "file not found" thrown
   """
   # Arrange

   # Act
   # Assert
   with pytest.raises(FileNotFoundError):
      DirectoryIterator(pathToDirectories = "NotExists")


def test_empty_repo_get_current_image_prompt_directory(fs: FakeFilesystem):
   """
   Given empty file repo
   When get_current_image_prompt_directory called
   Then returned directory is none
   """
   # Arrange
   fsState = {}
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   firstDirectory = directoryIterator.get_current_image_prompt_directory()

   # Assert
   assert firstDirectory is None


def test_empty_repo_get_next_time_prompt_directories(fs: FakeFilesystem):
   """
   Given empty file repo
   When get_next_time_prompt_directories called
   Then returned directory is none
   """
   # Arrange
   fsState = {}
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   nextDirectory = directoryIterator.get_next_time_prompt_directories()

   # Assert
   assert nextDirectory is None



def test_one_time_prompt_get_current_image_prompt_directory(fs: FakeFilesystem):
   """
   Given single prompt entry
   When get_current_image_prompt_directory called
   Then single prompt entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   firstDirectory = directoryIterator.get_current_image_prompt_directory()

   # Assert
   assert firstDirectory.date == "2024-01-14"
   assert firstDirectory.time == "03:03:45.522668"
   assert firstDirectory.prompt == "Shrek Eat Chips"
   assert firstDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_one_time_prompt_get_next_time_prompt_directories(fs: FakeFilesystem):
   """
   Given single prompt entry and directory iterator set to start backwards
   When get_next_time_prompt_directories called
   Then single prompt entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)

   # Act
   firstDirectory = directoryIterator.get_next_time_prompt_directories(direction = DIRECTION.BACKWARD)

   # Assert
   assert firstDirectory.date == "2024-01-14"
   assert firstDirectory.time == "03:03:45.522668"
   assert firstDirectory.prompt == "Shrek Eat Chips"
   assert firstDirectory.repo == TEST_RESOURCES_FOLDER_NAME

     
def test_one_time_prompt_get_current_image_prompt_directory(fs: FakeFilesystem):
   """
   Given single prompt entry
   When get_current_image_prompt_directory called
   Then nothing returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   nextDirectory = directoryIterator.get_current_image_prompt_directory()

   # Assert
   assert nextDirectory is None


def test_two_time_prompt_get_next_time_prompt_directories(fs: FakeFilesystem):
   """
   Given two prompt entries
   When get_next_time_prompt_directories called
   Then most recent entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   firstDirectory = directoryIterator.get_next_time_prompt_directories()

   # Assert
   assert firstDirectory.date == "2024-01-14"
   assert firstDirectory.time == "03:03:45.522668"
   assert firstDirectory.prompt == "Shrek Eat Chips"
   assert firstDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_two_time_prompt_get_current_image_prompt_directory(fs: FakeFilesystem):
   """
   Given two prompt entries and directory iterator set to start backwards
   When get_current_image_prompt_directory called
   Then least recent entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   firstDirectory = directoryIterator.get_next_time_prompt_directories(direction = DIRECTION.BACKWARD)

   # Assert
   assert firstDirectory.date == "2024-01-14"
   assert firstDirectory.time == "01:03:45.522668"
   assert firstDirectory.prompt == "Donkey Eat Chips"
   assert firstDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_two_time_prompt_get_next_time_prompt_directories(fs: FakeFilesystem):
   """
   Given two prompt entries
   When get_next_time_prompt_directories called
   Then 2nd most recent entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   directoryIterator.get_next_time_prompt_directories()
   nextDirectory = directoryIterator.get_next_time_prompt_directories()

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.time == "01:03:45.522668"
   assert nextDirectory.prompt == "Donkey Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_two_time_prompt_get_next_time_prompt_directories(fs: FakeFilesystem):
   """
   Given two prompt entries and directory iterator set to start backwards
   When backwards get_next_time_prompt_directories called
   Then most recent entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   directoryIterator.get_next_time_prompt_directories(direction = DIRECTION.BACKWARD)
   nextDirectory = directoryIterator.get_next_time_prompt_directories(direction = DIRECTION.BACKWARD)

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.prompt == "Shrek Eat Chips"
   assert nextDirectory.time == "03:03:45.522668"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_two_date_get_next_time_prompt_directories(fs: FakeFilesystem):
   """
   Given two prompt entries across dates
   When get_next_time_prompt_directories called
   Then entry in the next date directory returned
   """
   # Arrange
   fsState = {
      "2024-01-13": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
      },
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   directoryIterator.get_next_time_prompt_directories()
   nextDirectory = directoryIterator.get_next_time_prompt_directories()

   # Assert
   assert nextDirectory.date == "2024-01-13"
   assert nextDirectory.time == "01:03:45.522668"
   assert nextDirectory.prompt == "Donkey Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_two_date_get_next_time_prompt_directories(fs: FakeFilesystem):
   """
   Given two prompt entries across dates and directory iterator set to start backwards
   When backwards get_next_time_prompt_directories called
   Then most recent entry returned
   """
   # Arrange
   fsState = {
      "2024-01-13": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
      },
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   directoryIterator.get_next_time_prompt_directories(direction = DIRECTION.BACKWARD)
   nextDirectory = directoryIterator.get_next_time_prompt_directories(direction = DIRECTION.BACKWARD)

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.time == "03:03:45.522668"
   assert nextDirectory.prompt == "Shrek Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME