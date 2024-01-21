from io import BytesIO
import logging
import openai
import requests
from imageProviders.ImageProvider import ImageProvider, ImageProviderResult
from PIL import Image


class DalleProvider(ImageProvider):
    """
    A superclass used to wrap APIs for web operations.

    Attributes
    ----------

    Methods
    -------
    get_image_from_string(prompt)
        Retrieves image from API. Returns PIL Image object. Returns 'None' object on failure
    """

    # inherits from Provider
    def __init__(self, key=None):
        super().__init__(key=key, keyname=key)
        self.openAiClient = openai.OpenAI(api_key=key)
        return
    

    def engine_name(self):
        return "Dall-e"


    def get_image_from_string(self, prompt) -> ImageProviderResult:
        logging.info("Generating image for prompt : " + prompt)
        img = None
        errorMessage = None
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
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            url = response.data[0].url
            logging.info("Generated image at : " + url)
            img = Image.open(BytesIO(requests.get(url).content))

        except openai.APIConnectionError as e:
            logging.error(e)
            errorMessage = "Unable to contact OpenAI. Internet or provider may be down."
        except openai.AuthenticationError as e:
            logging.error(e)
            errorMessage = "Error authenticating with OpenAI. Please check your credentials in '.creds'."
        except openai.RateLimitError as e:
            logging.error(e)
            errorMessage = "OpenAI reporting Rate Limiting. Please check your account at openai.com."
        except openai.APITimeoutError as e:
            logging.error(e)            
            errorMessage = "Timeout contacting OpenAI. Internet or provider may be down."
        except BaseException as e:
            logging.error(e)
            errorMessage = str(e)
        
        return { 'img': img, 'errorMessage': errorMessage }
    
