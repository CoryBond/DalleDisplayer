
"""
Integration Tests For Inter-page interactrivity and high level applicaiton behavior
"""
import pytest
from unittest.mock import Mock   
from pathlib import Path
import os

from depdencyInjection.Container import Container

from pytestqt.qtbot import QtBot

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from ui.QApplicationManager import QApplicationManager
from dependencyInjection.containerTestUtil import override_with_mock_image_provider
from utils.loggingUtils import configureBasicLogger

from constantsTestUtil import TEST_RESOURCES_FOLDER_NAME, TEST_CONFIG, TEST_RESOURCES_FOLDER_PATH
from repoManager.test_DirectoryIterator import populate_fs_with

from pyfakefs.fake_filesystem import FakeFilesystem 


@pytest.fixture
def mockQApplicationManager(qapp):
   mock = Mock(spec=QApplicationManager)
   mock.getQApp = lambda : qapp
   return mock


@pytest.mark.timeout(10)
def test_home_page_loads_with_default_state(fs: FakeFilesystem, qtbot: QtBot, mockQApplicationManager):
   """
   Given lots of prompt entries
   When many subsequent calls to get_images with token provided (and backwards)
   Then result of the next page returned (sorted by most recent entries)
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)

   # Override with fake image provider.... temp turn of fs so we can access files for the
   # image provider to use 
   fs.pause()
   override_with_mock_image_provider(container)
   container.qApplicationManager.override(mockQApplicationManager)
   fs.resume()

   # Setup fake file system
   fsState = {}
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_PATH/"testRepo", fsState)

   # Act
   container.uiOrchestrator().start_with_bot(qtbot)

   # Assert   
   mainWindow = container.mainWindow()
   while ( mainWindow.isVisible() is False ):
      QTest.qWait(200)

   assert container.home().imageViewer.has_photo() is False


@pytest.mark.timeout(25)
def test_home_page_image_generation_refreshes_gallery(fs: FakeFilesystem, qtbot: QtBot, mockQApplicationManager):
   """
   Given lots of prompt entries
   When many subsequent calls to get_images with token provided (and backwards)
   Then result of the next page returned (sorted by most recent entries)
   """

   # Arrange
   container = Container()
   container.config.from_yaml(TEST_CONFIG.as_posix())
   container.config.repos.imageReposPath.from_value(TEST_RESOURCES_FOLDER_NAME)

   # Override with fake image provider.... temp turn of fs so we can access files for the
   # image provider to use 
   fs.pause()
   override_with_mock_image_provider(container)
   container.qApplicationManager.override(mockQApplicationManager)
   fs.resume()

   # Setup fake file system
   fsState = {}
   populate_fs_with(fs, TEST_RESOURCES_FOLDER_PATH/"testRepo", fsState)
   container.uiOrchestrator().start_with_bot(qtbot)

   mainWindow = container.mainWindow()
   while ( mainWindow.isVisible() is False ):
      QTest.qWait(200)

   homePage = container.home()

   # Act
   QTest.keyClicks(homePage.imageGenerator.promptbox, "some prompt")
   QTest.mouseClick(homePage.imageGenerator.generateImageButton, Qt.LeftButton)
   
   while ( container.gallery().gallery.contentWidget.layout().count() == 0 ):
      QTest.qWait(200)

   # Assert
   imagerow = container.gallery().gallery.contentWidget.layout().itemAt(0).widget()
   assert imagerow is not None
   assert imagerow.image_meta.prompt == "some prompt"
