from io import BytesIO
import logging
import openai
import requests
from imageProviders.ImageProvider import ImageProvider
from PIL import Image

from utils.loggingUtils import generate_logger


class DalleProvider(ImageProvider):


    # inherits from Provider
    def __init__(self, key=None):
        super().__init__(key=key, keyname=key)

        self.logger = generate_logger(self.__class__.__name__)

        self.openAiClient = openai.OpenAI(api_key=key)

        return


    def get_image_from_string(self, text, height=0, width=0) -> Image:
        self.logger.info("Generating image for text : " + text)
        try:
            # Select appropriate size from options in
            # res = list(DalleConst.SIZES.value.keys())[0]

            # if height != 0 and width != 0:
            #    for key in DalleConst.SIZES.value:
            #        if key > height or key > width:
            #            res = DalleConst.SIZES.value[key]
            #            break

            response = self.openAiClient.images.generate(
                model="dall-e-3",
                prompt="A cool turtle dude",
                size="1024x1024",
                quality="standard",
                n=1,
            )

            url = response.data[0].url
            self.logger.info("Generated image at : " + url)
            img = Image.open(BytesIO(requests.get(url).content))

        except BaseException as e:
            self.logger.error(e)
            return None
        
        # img.save("test.png", "PNG");

        return img