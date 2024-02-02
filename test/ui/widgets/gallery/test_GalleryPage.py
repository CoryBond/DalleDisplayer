
"""
Integration Tests For Gallery Page
"""
import pytest
from depdencyInjection.Container import Container

from pytestqt.qtbot import QtBot

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from repoManager.test_DirectoryIterator import populate_fs_with

from pyfakefs.fake_filesystem import FakeFilesystem 


@pytest.mark.timeout(10)
def test_gallery_loads_correctly(containerWithMocks: Container, qtbot: QtBot, fs: FakeFilesystem):
    """
    Given lots of prompt entries
    When many subsequent calls to get_images with token provided (and backwards)
    Then result of the next page returned (sorted by most recent entries)
    """

    # Arrange
    repoManager = containerWithMocks.repoManager()

    # Setup fake file system
    fsState = {}
    populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)

    # Act
    gallery = containerWithMocks.gallery()
    qtbot.addWidget(gallery)
    gallery.show()

    # Assert   
    while ( gallery.isVisible() is False ):
        QTest.qWait(200)

    assert gallery.gallery.contentWidget.layout().count() == 0
    assert gallery.forward_page_button.isEnabled() is False
    assert gallery.backward_page_button.isEnabled() is False
    assert gallery.current_page.text == "1"


@pytest.mark.timeout(20)
def test_gallery_loads_with_images(containerWithMocks: Container, qtbot: QtBot, fs: FakeFilesystem):
    """
    Given lots of prompt entries
    When many subsequent calls to get_images with token provided (and backwards)
    Then result of the next page returned (sorted by most recent entries)
    """

    # Arrange
    repoManager = containerWithMocks.repoManager()

    # Setup fake file system
    fsState = {
        "2024-01-14": { 
            "01:03:45.522668_Donkey Eat Chips0": ["1.png"], # first page
            "03:03:45.522668_Shrek Eat Chips1": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips2": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips3": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips4": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips5": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips6": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips7": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips8": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips9": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips10": ["1.png"], # second page
        }
    }
    populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)
    
    # Act
    gallery = containerWithMocks.gallery()
    qtbot.addWidget(gallery)
    gallery.show()

    # Assert   
    while ( gallery.isVisible() is False ):
        QTest.qWait(200)

    assert gallery.forward_page_button.isEnabled()
    assert gallery.backward_page_button.isEnabled() is False

    assert gallery.gallery.contentWidget.layout().count() == 10
    assert gallery.gallery.contentWidget.layout().itemAt(0).widget() is not None
    assert gallery.gallery.contentWidget.layout().itemAt(1).widget() is not None
    assert gallery.current_page.text == "1"


@pytest.mark.timeout(40)
def test_gallery_forward_button_click(containerWithMocks: Container, qtbot: QtBot, fs: FakeFilesystem):
    """
    Given lots of prompt entries
    When many subsequent calls to get_images with token provided (and backwards)
    Then result of the next page returned (sorted by most recent entries)
    """

    # Arrange
    repoManager = containerWithMocks.repoManager()

    # Setup fake file system
    fsState = {
        "2024-01-14": { 
            "01:03:45.522668_Donkey Eat Chips0": ["1.png"], # first page
            "03:03:45.522668_Shrek Eat Chips1": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips2": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips3": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips4": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips5": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips6": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips7": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips8": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips9": ["1.png"],
            "03:03:45.522668_Shrek Eat Chips10": ["1.png"], # second page
            "03:03:45.522668_Shrek Eat Chips11": ["1.png"],
        }
    }
    populate_fs_with(fs, repoManager.current_repo_abs_path(), fsState)

    gallery = containerWithMocks.gallery()
    qtbot.addWidget(gallery)
    gallery.show()
    while ( gallery.isVisible() is False ):
        QTest.qWait(200)

    # Act
    QTest.mouseClick(gallery.forward_page_button, Qt.LeftButton)

    # Assert
    while ( gallery.forward_page_button.isEnabled() ):
        QTest.qWait(200)

    assert gallery.forward_page_button.isEnabled() is False
    assert gallery.backward_page_button.isEnabled()
    assert gallery.gallery.contentWidget.layout().count() == 2
    assert gallery.gallery.contentWidget.layout().itemAt(0).widget() is not None
    assert gallery.gallery.contentWidget.layout().itemAt(1).widget() is not None
    assert gallery.current_page.text == "2"
