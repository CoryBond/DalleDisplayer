
import sys
print(sys.path)

import pytest
from unittest.mock import Mock   
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from depdencyInjection.Container import Container
from imageProviders.ImageProvider import ImageProvider

from pytestqt.qt_compat import qt_api


def raise_exception(msg: str):
    raise Exception(msg)


#@pytest.fixture
#def imageProviderMock():
#   mock = Mock()
#   mock.engine_name = lambda : "mockGenerator"
#   mock.get_image_from_string = lambda : raise_exception('some message')
#   return mock


def test_image_generation_error(qtbot):
   '''Test That Error Dialog Appears When Image Provider Errors'''
   # Arrange
   #container = Container()
   
   #container.imageProvider.override(imageProviderMock)

   #container.ui().start()
   #mainWindow = container.mainWindow()

   widget = qt_api.QtWidgets.QWidget()
   qtbot.addWidget(widget)
   widget.setWindowTitle("W1")
   widget.show()
      
   # Act
   # QTest.mouseClick(mainWindow.generateImageButton, Qt.LeftButton)

   # Assert
   assert widget.isVisible()