
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

def test_kkkk():
    print("")