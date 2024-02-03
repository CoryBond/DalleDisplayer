from typing import TypedDict


ImageProviderResult = TypedDict('ImageProviderResult', {
    'img': bytes,
    'errorMessage': str,
})


class ImageProvider(object):
    """
    A superclass used to wrap APIs for web operations.

    Attributes
    ----------

    Methods
    -------
    get_image_from_string(prompt)
        Retrieves image from API. Returns PIL Image object. Returns 'None' object on failure
    """
    def __init__(self, key=None, keyname=None):
        self.key = key
        self.keyname = keyname
        self.host = None
        return
    

    def engine_name(self) -> str:
        return


    def get_image_from_string(self, prompt) -> ImageProviderResult:
        return
    
