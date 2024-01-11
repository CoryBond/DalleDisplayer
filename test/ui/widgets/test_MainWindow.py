
import sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent.parent.parent.as_posix()+"/src") # Add src directory to python path so we can access src modules
print(sys.path)

import unittest
from unittest.mock import patch                                       
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from depdencyInjection.Container import Container
from imageProviders.ImageProvider import ImageProvider


def raise_exception(msg: str):
    raise Exception(msg)


class TestMainWindow(unittest.TestCase):


   def setUp(self):
      '''Setup Container'''
      self.container = Container()


   def test_lala(self):
      return


   @patch('imageProviders.ImageProvider')
   def test_image_generation_error(self, imageProvider: ImageProvider):
      '''Test That Error Dialog Appears When Image Provider Errors'''
      # Arrange

      imageProvider.engine_name = lambda : "mockGenerator"
      imageProvider.get_image_from_string = lambda : raise_exception('some message')
      self.container.imageProvider.override(imageProvider)

      self.container.ui().start()
      mainWindow = self.container.mainWindow()
      
      # Act
      QTest.mouseClick(mainWindow.generateImageButton, Qt.LeftButton)

      # Assert
      self.assertTrue(mainWindow.errorDialog.isVisible())


if __name__ == '__main__':
    unittest.main()