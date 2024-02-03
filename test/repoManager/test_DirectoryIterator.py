import pytest

from repoManager.DirectoryIterator import DirectoryIterator
from repoManager.Models import ImagePromptDirectory

from utils.enums import DIRECTION


TEST_RESOURCES_FOLDER_NAME = "testResources"


def test_exception_thrown_on_existant_directory(fshelpers):
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


def test_empty_repo_next(fshelpers):
   """
   Given empty file repo
   When next called
   Then iterator exhausted
   """
   # Arrange
   fsState = {}
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)

   # Assert
   try:
       next(directoryIterator)
   except StopIteration:
      assert True
   else:
      assert False


def test_backwards_one_time_prompt_next(fshelpers):
   """
   Given single prompt entry and directory iterator set to start backwards
   When next called
   Then single prompt entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, direction = DIRECTION.BACKWARD)

   # Act
   firstDirectory = next(directoryIterator)

   # Assert
   assert firstDirectory.date == "2024-01-14"
   assert firstDirectory.time == "03:03:45.522668"
   assert firstDirectory.prompt == "Shrek Eat Chips"
   assert firstDirectory.repo == TEST_RESOURCES_FOLDER_NAME

     
def test_exhausting_iterator(fshelpers):
   """
   Given single prompt entry
   When next called till exhuastion
   Then iterator exhausted
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   next(directoryIterator)

   # Assert
   try:
       next(directoryIterator)
   except StopIteration:
      assert True
   else:
      assert False



def test_two_time_prompt_next(fshelpers):
   """
   Given two prompt entries
   When next called
   Then most recent entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   firstDirectory = next(directoryIterator)

   # Assert
   assert firstDirectory.date == "2024-01-14"
   assert firstDirectory.time == "03:03:45.522668"
   assert firstDirectory.prompt == "Shrek Eat Chips"
   assert firstDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_two_time_prompt_get_second_time_prompt_directories(fshelpers):
   """
   Given two prompt entries
   When next called
   Then 2nd most recent entry returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   next(directoryIterator)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.time == "01:03:45.522668"
   assert nextDirectory.prompt == "Donkey Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_two_time_prompt_next(fshelpers):
   """
   Given two prompt entries and directory iterator set to start backwards
   When multiple next called
   Then next next entry is returned
   """
   # Arrange
   fsState = {
      "2024-01-14": { 
         "01:03:45.522668_Donkey Eat Chips": ["1.png"],
         "03:03:45.522668_Shrek Eat Chips": ["1.png"]
      }
   }
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, direction = DIRECTION.BACKWARD)
   next(directoryIterator)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.prompt == "Shrek Eat Chips"
   assert nextDirectory.time == "03:03:45.522668"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_two_date_next(fshelpers):
   """
   Given two prompt entries across dates
   When multiple next called
   Then next next entry is returned
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME)
   next(directoryIterator)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-13"
   assert nextDirectory.time == "01:03:45.522668"
   assert nextDirectory.prompt == "Donkey Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_two_date_next(fshelpers):
   """
   Given two prompt entries across dates, iterator set to backwards and directory iterator set to start backwards
   When multiple next called
   Then next next entry is returned
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, direction = DIRECTION.BACKWARD)
   next(directoryIterator)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.time == "03:03:45.522668"
   assert nextDirectory.prompt == "Shrek Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_starting_directory_provided(fshelpers):
   """
   Given two prompt entries across dates and starting directory is at the front
   When next called
   Then first directory returned
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   startingDirectory = ImagePromptDirectory(
      prompt="blah blah",
      time="23:59:59.522668",
      repo="doesn't matter",
      date="2024-01-14",
   )

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, startingDirectory=startingDirectory)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.time == "03:03:45.522668"
   assert nextDirectory.prompt == "Shrek Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_starting_directory_in_middle_provided(fshelpers):
   """
   Given two prompt entries across dates and starting directory is in the middle
   When next called
   Then next directory is returned
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   startingDirectory = ImagePromptDirectory(
      prompt="blah blah",
      time="00:59:59.522668",
      repo="doesn't matter",
      date="2024-01-14",
   )

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, startingDirectory=startingDirectory)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-13"
   assert nextDirectory.time == "01:03:45.522668"
   assert nextDirectory.prompt == "Donkey Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_starting_directory_at_end_provided(fshelpers):
   """
   Given two prompt entries across dates and starting directory is at the end
   When next called
   Then iterator is exhausted
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   startingDirectory = ImagePromptDirectory(
      prompt="Donkey Eat Chips",
      time="01:03:45.522668",
      repo="doesn't matter",
      date="2024-01-13",
   )

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, startingDirectory=startingDirectory)

   # Assert
   try:
       next(directoryIterator)
   except StopIteration:
      assert True
   else:
      assert False


def test_backwards_starting_directory_at_end_provided(fshelpers):
   """
   Given two prompt entries across dates, iterator going backwards and starting directory is at the end
   When next called
   Then end directory returned
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   startingDirectory = ImagePromptDirectory(
      prompt="blah blah",
      time="00:59:59.522668",
      repo="doesn't matter",
      date="2024-01-12",
   )

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, startingDirectory=startingDirectory, direction = DIRECTION.BACKWARD)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-13"
   assert nextDirectory.time == "01:03:45.522668"
   assert nextDirectory.prompt == "Donkey Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_starting_directory_in_middle_provided(fshelpers):
   """
   Given two prompt entries across dates, iterator going backwards and starting directory is in the middle
   When next called
   Then next entry returned
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   startingDirectory = ImagePromptDirectory(
      prompt="blah blah",
      time="00:59:59.522668",
      repo="doesn't matter",
      date="2024-01-14",
   )

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, startingDirectory=startingDirectory, direction = DIRECTION.BACKWARD)
   nextDirectory = next(directoryIterator)

   # Assert
   assert nextDirectory.date == "2024-01-14"
   assert nextDirectory.time == "03:03:45.522668"
   assert nextDirectory.prompt == "Shrek Eat Chips"
   assert nextDirectory.repo == TEST_RESOURCES_FOLDER_NAME


def test_backwards_starting_directory_provided(fshelpers):
   """
   Given two prompt entries across dates, iterator going backwards and starting directory is at the beginning
   When next called
   Then iterator exhausted
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
   fshelpers.populate_fs_with(TEST_RESOURCES_FOLDER_NAME, fsState)

   startingDirectory = ImagePromptDirectory(
      prompt="Shrek Eat Chips",
      time="03:03:45.522668",
      repo="doesn't matter",
      date="2024-01-14",
   )

   # Act
   directoryIterator = DirectoryIterator(pathToDirectories = TEST_RESOURCES_FOLDER_NAME, startingDirectory=startingDirectory, direction = DIRECTION.BACKWARD)

   # Assert
   try:
       next(directoryIterator)
   except StopIteration:
      assert True
   else:
      assert False
