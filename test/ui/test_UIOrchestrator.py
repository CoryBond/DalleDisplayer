
"""
Integration Tests For Inter-page interactrivity and high level applicaiton behavior
"""
import pytest

from depdencyInjection.Container import Container

from pytestqt.qtbot import QtBot

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from pyfakefs.fake_filesystem import FakeFilesystem 
from utils_for_test import populate_fs_with


@pytest.mark.timeout(10)
def test_home_page_loads_with_default_state(containerWithMocks: Container, qtbot: QtBot, fs: FakeFilesystem):
   """
   Given application
   When loaded for the very first time
   Then default homepage shows up
   """

   # Arrange
   # Setup fake file system
   repoConfiguredPath = containerWithMocks.repoManager().current_repo_abs_path()
   fsState = {}
   populate_fs_with(fs,repoConfiguredPath, dateDictStructure=fsState)


   # Act
   containerWithMocks.uiOrchestrator().start_with_bot(qtbot)

   # Assert   
   mainWindow = containerWithMocks.mainWindow()
   while ( mainWindow.isVisible() is False ):
      QTest.qWait(200)

   assert containerWithMocks.home().imageViewer.has_photo() is False


@pytest.mark.timeout(25)
def test_home_page_image_generation_refreshes_gallery(containerWithMocks: Container, qtbot: QtBot, fs: FakeFilesystem):
   """
   Given application
   When user clicks generate image
   Then gallery page refreshes
   """

   # Arrange

   # Setup fake file system
   repoConfiguredPath = containerWithMocks.repoManager().current_repo_abs_path()
   fsState = {}
   populate_fs_with(fs,repoConfiguredPath, dateDictStructure=fsState)
   containerWithMocks.uiOrchestrator().start_with_bot(qtbot)

   mainWindow = containerWithMocks.mainWindow()
   while ( mainWindow.isVisible() is False ):
      QTest.qWait(200)

   homePage = containerWithMocks.home()

   # Act
   QTest.keyClicks(homePage.imageGenerator.promptbox, "some prompt")
   QTest.mouseClick(homePage.imageGenerator.generateImageButton, Qt.LeftButton)
   
   while ( containerWithMocks.gallery().gallery.contentWidget.layout().count() == 0 ):
      QTest.qWait(200)

   # Assert
   imagerow = containerWithMocks.gallery().gallery.contentWidget.layout().itemAt(0).widget()
   assert imagerow is not None
   assert imagerow.image_meta.prompt == "some prompt"
