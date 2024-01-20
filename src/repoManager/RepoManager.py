import logging
import os
from pathlib import Path

from utils.dateUtils import get_current_sortable_datetime_strs
from utils.pathingUtils import get_or_create_image_repos
from PIL import Image


class ImageResult(object):
    def __init__(self, prompt: str, repo: str, date: str, time: str, num: int, pngPath: Path):
        self.prompt = prompt
        self.repo = repo
        self.date = date
        self.time = time
        self.num = num
        self.pngPath = pngPath


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


    def current_repo(self):
        return self.imageRepo.name


    def switch_repo(self, newRepo: str):
        self.imageRepo = get_or_create_image_repos()/newRepo


    def generate_png_path(self, prompt: str) -> ImageResult:
        dateTimeSegments = get_current_sortable_datetime_strs()
        dayDirectory = self.imageRepo/dateTimeSegments[0]

        promptWithTime = dateTimeSegments[1] + "_" + prompt
        promptAbsPath = dayDirectory/promptWithTime
        promptAbsPath.mkdir( parents=True, exist_ok=True )

        return ImageResult(
            prompt,
            repo=self.current_repo(),
            date=dateTimeSegments[0],
            time=dateTimeSegments[1],
            num="1",
            pngPath=promptAbsPath/"1.png"
        )

    
    def get_latest_image_posix_in_repo(self) -> ImageResult:
        try:
            imageDates = os.listdir(self.imageRepo)
            lastImageDate = imageDates[0]
            lastDateImagePrompts = os.listdir(self.imageRepo/lastImageDate)
            lastImagePrompt = lastDateImagePrompts[0]

            pathToLastImagePrompt = self.imageRepo/lastImageDate/lastImagePrompt

            lastImagePromptPosix = (pathToLastImagePrompt/"1.png").as_posix()

            logging.info("Found last image prompt of repo : " + lastImagePromptPosix)

            time, prompt = lastImagePrompt.split("_")
            return ImageResult(
                prompt=prompt,
                repo=self.current_repo(),
                date=lastImageDate,
                time=time,
                num="1",
                pngPath=lastImagePromptPosix
            )
        except BaseException as e:
            logging.warning(e)
            return None


    def save_image(self, prompt: str, image: Image) -> ImageResult:
        result = self.generate_png_path(prompt)
        image.save(result.pngPath, "PNG")
        return result
