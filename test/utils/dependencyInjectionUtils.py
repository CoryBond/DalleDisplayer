from unittest.mock import patch, MagicMock                                       
from depdencyInjection.Container import Container
from imageProviders.ImageProvider import ImageProvider
from PIL import Image

from utils.pathingUtils import get_project_root

def testImageGenerator():
        i = 0
        def cb(prompt: str) -> Image:
            nonlocal i 
            i += 1
            testFile = "test1.png" if i % 2 == 0 else "test2.png"
            return Image.open(get_project_root()/'..'/'testResources'/'images'/'ai'/testFile)
        return cb


@patch('imageProviders.ImageProvider')
def override(container: Container, imageProvider: ImageProvider):

    imageProvider.engine_name = lambda : "mockGenerator"
    imageProvider.get_image_from_string = testImageGenerator()

    container.imageProvider.override(imageProvider)
    return