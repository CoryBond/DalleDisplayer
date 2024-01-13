import time
from unittest.mock import patch                                       
from depdencyInjection.Container import Container
from imageProviders.ImageProvider import ImageProvider
from PIL import Image

from utils.pathingUtils import get_project_root


def test_image_generator():
        i = 0
        def cb(prompt: str) -> Image:
            nonlocal i 
            i += 1
            time.sleep(4)
            testFile = "test1.png" if i % 2 == 0 else "test2.png"
            img = Image.open(get_project_root()/'..'/'testResources'/'images'/'ai'/testFile)
            return { 'img': img, 'errorMessage': None }
        return cb


@patch('imageProviders.ImageProvider')
def override_with_mock_image_provider(container: Container, imageProvider: ImageProvider):

    imageProvider.engine_name = lambda : "mockGenerator"
    imageProvider.get_image_from_string = test_image_generator()

    container.imageProvider.override(imageProvider)
    return
