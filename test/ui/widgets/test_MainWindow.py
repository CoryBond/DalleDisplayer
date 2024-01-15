
import pytest
from unittest.mock import Mock   
import logging

from depdencyInjection.Container import Container

from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
from pytestqt.qtbot import QtBot

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from ui.QApplicationManager import QApplicationManager
from dependencyInjection.containerTestUtil import override_with_mock_image_provider
from utils.loggingUtils import configureBasicLogger


configureBasicLogger(filename="test_aiImageDisplayer.log", level=logging.DEBUG)


def raise_exception(msg: str):
    raise Exception(msg)


@pytest.fixture
def mockQApplicationManager(qapp):
   mock = Mock(spec=QApplicationManager)
   mock.getQApp = lambda : qapp
   return mock


@pytest.mark.timeout(10)
def test_home_page_loads_with_default_state(qtbot: QtBot, mockQApplicationManager):
   '''Test That Error Dialog Appears When Image Provider Errors'''

   # Arrange
   container = Container()
   override_with_mock_image_provider(container)   
   container.qApplicationManager.override(mockQApplicationManager)
      
   # Act
   container.uiOrchestrator().start_with_bot(qtbot)

   # Assert   
   mainWindow = container.mainWindow()
   while ( mainWindow.isVisible() is False ):
      QTest.qWait(200)

   assert mainWindow.generateImageButton.isEnabled() is False


@pytest.mark.timeout(10)
def test_image_generation_loads_image(qtbot: QtBot, mockQApplicationManager):
   '''Test That Error Dialog Appears When Image Provider Errors'''

   # Arrange
   container = Container()
   override_with_mock_image_provider(container)   
   container.qApplicationManager.override(mockQApplicationManager)

   container.uiOrchestrator().start_with_bot(qtbot)
   mainWindow = container.mainWindow()

   while ( mainWindow.isVisible() is False ):
      QTest.qWait(20000)
      
   # Act
   QTest.keyClicks(mainWindow.promptbox, "some prompt")
   QTest.mouseClick(mainWindow.generateImageButton, Qt.LeftButton)

   # Assert
   assert mainWindow.imageViewer.has_photo()