"""
Test config file for UI code
"""
import pytest
from unittest.mock import Mock   

from ui.QApplicationManager import QApplicationManager

@pytest.fixture
def mockQApplicationManager(qapp):
   mock = Mock(spec=QApplicationManager)
   mock.getQApp = lambda : qapp
   return mock


# Overrides containerWithMocks with more UI specific mocks
@pytest.fixture
def containerWithMocks(containerWithMocks, mockQApplicationManager):
   containerWithMocks.qApplicationManager.override(mockQApplicationManager)
   return containerWithMocks