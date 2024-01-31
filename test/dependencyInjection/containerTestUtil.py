import time
from unittest.mock import patch                                       
from depdencyInjection.Container import Container
from imageProviders.ImageProvider import ImageProvider, ImageProviderResult
from PIL import Image

from utils.pathingUtils import get_project_root





def test_image_generator():
        """
        Simulates a image getting generting by loading an existing image from the testResources folder.
        Will also simulate "lag" by sleeping the current thread.
        Should be run in a seperate thread as to prevent UI event loop from being freezed as well.
        """
        TestFile1 = Image.open(get_project_root()/'..'/'testResources'/'images'/'ai'/"test1.png")
        TestFile2 = Image.open(get_project_root()/'..'/'testResources'/'images'/'ai'/"test2.png")
        i = 0
        def cb(prompt: str) -> ImageProviderResult:
            nonlocal i 
            i += 1
            time.sleep(4)
            img = TestFile1 if i % 2 == 0 else TestFile2
            return { 'img': img, 'errorMessage': None }
        return cb


@patch('imageProviders.ImageProvider')
def override_with_mock_image_provider(container: Container, imageProvider: ImageProvider):
    """
    Creates a generic mock of ImageProvider and adds it to the dependency injection container
    """
    imageProvider.engine_name = lambda : "mockGenerator"
    imageProvider.get_image_from_string = test_image_generator()

    container.imageProvider.override(imageProvider)
    return