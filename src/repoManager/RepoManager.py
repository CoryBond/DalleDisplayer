import logging
import os
from pathlib import Path

from utils.dateUtils import get_current_sortable_datetime_strs
from utils.pathingUtils import get_or_create_image_repos
from PIL import Image


class RepoManager(object):


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
            logging.error(e)
            return None


    def save_image(self, prompt: str, image: Image) -> Path:
        pngPath = self.generate_png_path(prompt)
        image.save(pngPath, "PNG")
        return pngPath
