import logging
import os
from pathlib import Path

from utils.dateUtils import get_current_sortable_datetime_strs
from utils.pathingUtils import get_or_create_image_repos
from PIL import Image


class RepoManager(object):
    """
    Class that manages a colleciton of AI image repositories set in a local file system.

    AI Image repos are saved by directory under "$HOME/PAIID/resources/imageRepos". Within each repo images
    are partitioned by date first. Per date the images are saved together under the prompt and time they were generated.
    So, for example, if we have a prompt "Sad rat" generate 2 images then they can be saved under the following path:
    "$HOME/PAIID/resources/imageRepos/Dall-e/2024-01-11/15:05:06.713451_Sad rat"

    When saving with this repo manager the entire path will be created and images will be stored there. Currently this
    repo manager does not allow configuring where imageRepos are managed.
    """

    def __init__(self, startingRepo: str):
        self.switch_repo(startingRepo)
        return


    def switch_repo(self, newRepo: str):
        self.imageRepo = get_or_create_image_repos()/newRepo


    def generate_png_path(self, prompt: str) -> Path:
        dateTimeSegments = get_current_sortable_datetime_strs()
        dayDirectory = self.imageRepo/dateTimeSegments[0]

        promptWithTime = dateTimeSegments[1] + "_" + prompt
        promptAbsPath = dayDirectory/promptWithTime
        promptAbsPath.mkdir( parents=True, exist_ok=True )

        return promptAbsPath/"1.png"

    
    def get_latest_image_posix_in_repo(self):
        try:
            imageDates = os.listdir(self.imageRepo)
            lastImageDate = imageDates[0]
            lastDateImagePrompts = os.listdir(self.imageRepo/lastImageDate)
            lastImagePrompt = lastDateImagePrompts[0]

            pathToLastImagePrompt = self.imageRepo/lastImageDate/lastImagePrompt

            lastImagePromptPosix = (pathToLastImagePrompt/"1.png").as_posix()

            logging.info("Found last image prompt of repo : " + lastImagePromptPosix)
            return lastImagePromptPosix
        except BaseException as e:
            logging.warning(e)
            return None


    def save_image(self, prompt: str, image: Image) -> Path:
        pngPath = self.generate_png_path(prompt)
        image.save(pngPath, "PNG")
        return pngPath
