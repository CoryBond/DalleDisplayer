import pytest
from typing import Dict, List

from utils.pathingUtils import DIRECTION
from utils.algoUtils import get_next_string_index_from_reverse_sorted

TimeWithPromptDictType = Dict[str, List[str]]
DateDictType = Dict[str, TimeWithPromptDictType]


def test_empty_folder_get_next_file_index_from_reverse_sorted():
    """
    Given empty folder and no file
    When get_next_file_index_from_reverse_sorted called
    Then no index returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "someFile", reverseSortedStrings = None)

    # Assert
    assert index is None


def test_backwards_empty_folder_get_next_file_index_from_reverse_sorted():
    """
    Given empty folder and no file
    When backwards get_next_file_index_from_reverse_sorted called
    Then no index returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "someFile", reverseSortedStrings = None, direction = DIRECTION.BACKWARD)

    # Assert
    assert index is None


def test_next_index_does_not_exist_folder_get_next_file_index_from_reverse_sorted():
    """
    Given current file does not have a next file
    When get_next_file_index_from_reverse_sorted called
    Then no index returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "2013", reverseSortedStrings = ["2013"])

    # Assert
    assert index is None


def test_backwards_next_index_does_not_exist_folder_get_next_file_index_from_reverse_sorted():
    """
    Given current file does not have a next file
    When backwards get_next_file_index_from_reverse_sorted called
    Then no index returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "2013", reverseSortedStrings = ["2013"], direction = DIRECTION.BACKWARD)

    # Assert
    assert index is None


def test_next_index_does_exist_folder_get_next_file_index_from_reverse_sorted():
    """
    Given current file does not have a next file
    When get_next_file_index_from_reverse_sorted called
    Then no index returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "2013", reverseSortedStrings = ["2012"])

    # Assert
    assert index == 0


def test_backwards_next_index_does_exist_folder_get_next_file_index_from_reverse_sorted():
    """
    Given current file does not have a next file
    When backwards get_next_file_index_from_reverse_sorted called
    Then no index returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "2013", reverseSortedStrings = ["2014"], direction = DIRECTION.BACKWARD)

    # Assert
    assert index == 0


def test_rewind_forward():
    """
    Given max file name
    When get_next_file_index_from_reverse_sorted called
    Then first forwards file returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "9999-99-99", reverseSortedStrings = ['2024-01-14', '2024-01-13'])
    index2 = get_next_string_index_from_reverse_sorted(theString = "9999-99-99", reverseSortedStrings = ['2024-01-14'])

    # Assert
    assert index == 0
    assert index2 == 0


def test_rewind_backwards():
    """
    Given min file name
    When backwards get_next_file_index_from_reverse_sorted called
    Then first backwards file returned
    """
    # Arrange

    # Act
    index = get_next_string_index_from_reverse_sorted(theString = "0000-00-00", reverseSortedStrings = ['2024-01-14', '2024-01-13'], direction = DIRECTION.BACKWARD)
    index2 = get_next_string_index_from_reverse_sorted(theString = "0000-00-00", reverseSortedStrings = ['2024-01-14'], direction = DIRECTION.BACKWARD)

    # Assert
    assert index == 1
    assert index2 == 0

