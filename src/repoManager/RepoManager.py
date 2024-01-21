from enum import Enum
import logging
import os
from pathlib import Path
from typing import List
from decorators.decorators import auto_str

from utils.dateUtils import get_current_sortable_datetime_strs
from utils.pathingUtils import get_or_create_image_repos, get_sorted_directory_by_name
from PIL import Image


@auto_str
class ImagePromptDirectory(object):
    def __init__(self, prompt: str, repo: str, date: str, time: str, absPath: str = None):
        self.prompt = prompt
        self.repo = repo
        self.date = date
        self.time = time
        self.absolutePath = absPath


@auto_str 
class NextToken(object):
    def __init__(self, prompt: str, repo: str, date: str, time: str):
        self.prompt = prompt
        self.repo = repo
        self.date = date
        self.time = time


@auto_str
class ImagePrompResult(object):
    def __init__(self, prompt: str, repo: str, date: str, time: str, num: int, pngPaths: List[Path]):
        self.prompt = prompt
        self.repo = repo
        self.date = date
        self.time = time
        self.num = num
        self.pngPaths = pngPaths


@auto_str
class GetImagePrompsResult(object):
    def __init__(self, results: List[ImagePrompResult], nextToken: NextToken):
        self.results = results
        self.nextToken = nextToken


class DIRECTION(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"


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
        self.imageRepo: Path = get_or_create_image_repos()/newRepo


    def generate_file_name(self, time: str, prompt: str):
        return time + "_" + prompt


    def generate_png_path(self, prompt: str) -> ImagePromptDirectory:
        date, time = get_current_sortable_datetime_strs()
        dayDirectory = self.imageRepo/date

        promptWithTime = self.generate_file_name(time, prompt)
        promptAbsPath = dayDirectory/promptWithTime
        promptAbsPath.mkdir( parents=True, exist_ok=True )

        return ImagePromptDirectory(
            prompt,
            repo=self.current_repo(),
            date=date,
            time=time,
            absPath=promptAbsPath
        )

    
    def get_files(self, date: str, folderName: str) -> ImagePrompResult:
        logging.info(f"Attempting to load images from {date} and folder {folderName}")
        time, prompt = folderName.split("_")
        pathToLastImagePrompt = self.imageRepo/date/folderName
        fullImagePaths = [pathToLastImagePrompt/file for file in os.listdir(pathToLastImagePrompt)]

        logging.debug(f"Found the images : {str(fullImagePaths)}")
        return ImagePrompResult(
            prompt=prompt,
            repo=self.current_repo(),
            date=date,
            time=time,
            num="1",
            pngPaths=fullImagePaths
        )


    def get_latest_images_in_repo(self) -> ImagePrompResult:
        logging.info("Attempting to load last image created")
        try:
            imageDates = get_sorted_directory_by_name(self.imageRepo)
            lastImageDate = imageDates[0]
            lastDateImagePrompts = get_sorted_directory_by_name(self.imageRepo/lastImageDate)
            lastImagePrompt = lastDateImagePrompts[0]

            return self.get_files(date=lastImageDate, folderName=lastImagePrompt)
        except BaseException as e:
            logging.warning(e)
            return None


    def get_next_image_folder(self, currentDirectory: ImagePromptDirectory, currentTimePromptDirectories: List[str], sortedDatesDirectory: List[str], direction: DIRECTION = DIRECTION.FORWARD) -> tuple[ImagePromptDirectory, : List[str]]:
        promptWithTime = self.generate_file_name(currentDirectory.time, currentDirectory.prompt)

        def index_not_out_of_bounds(index: int, directory: List[str]):
            return direction is DIRECTION.FORWARD and index < len(currentTimePromptDirectories) or direction is DIRECTION.BACKWARD and index >= 0
        
        # To support going forward or backward
        nextIndex = 1 if direction is not DIRECTION.BACKWARD else -1

        nextImageIndex = currentTimePromptDirectories.index(promptWithTime) + nextIndex
        currentImageTime = currentDirectory.time
        currentPrompt = currentDirectory.prompt
        currentImageDate = currentDirectory.date
        if(index_not_out_of_bounds(nextImageIndex, currentTimePromptDirectories)):
            currentImageFolder = currentTimePromptDirectories[nextImageIndex]
            currentImageTime, currentPrompt = currentImageFolder.split("_")
        else:
            # go to the next date as this directory is exhausted
            nextDateIndex = sortedDatesDirectory.index(currentImageDate) + nextIndex
            if(index_not_out_of_bounds(nextDateIndex, sortedDatesDirectory)):
                currentImageDate = sortedDatesDirectory[nextDateIndex]
                currentTimePromptDirectories = get_sorted_directory_by_name(self.imageRepo/currentImageDate)
                startIndexOfNextDateFolder = 0 if direction is not DIRECTION.BACKWARD else len(currentTimePromptDirectories)-1
                currentImageTime, currentPrompt = currentTimePromptDirectories[startIndexOfNextDateFolder].split("_")
            else:
                # We have exhausted all directories! No Directory can be returned
                return [None, currentTimePromptDirectories]
        return [
            ImagePromptDirectory(
                prompt=currentPrompt,
                repo=self.current_repo(),
                date=currentImageDate,
                time=currentImageTime
            ), 
            currentTimePromptDirectories
        ]


    def get_init_images(self, number: int) -> GetImagePrompsResult:
        result = self.get_latest_images_in_repo()
        firstDirectory = ImagePromptDirectory(
            prompt=result.prompt,
            repo=self.imageRepo,
            date=result.date,
            time=result.time
        )

        return self._get_images(number, firstDirectory, direction=DIRECTION.FORWARD, forceIncludeCurrentDirectoryInResults=True)


    def get_images(self, number: int, token: NextToken, direction: DIRECTION = DIRECTION.FORWARD) -> GetImagePrompsResult:
        validToken = None
        if token is not None:
            logging.debug(f"Provided token : {token}")
            validToken = token
            return self._get_images(number, validToken, direction)
        else:
            logging.warn(f"No images will be returned due to invalid token {token}")
            return None


    def _get_images(self, number: int, currentDirectory: ImagePromptDirectory, direction: DIRECTION = DIRECTION.FORWARD, forceIncludeCurrentDirectoryInResults: bool = False) -> GetImagePrompsResult:
        logging.info("Getting images")

        imagePromptResults: List[ImagePrompResult] = []

        sortedDatesDirectory = get_sorted_directory_by_name(self.imageRepo)
        currentTimePromptDirectories = get_sorted_directory_by_name(self.imageRepo/currentDirectory.date)

        def generate_nextToken(imagePromptResults: list[ImagePrompResult]):
            nextToken = None
            if (len(imagePromptResults) == number):
                directoryToTokenize = imagePromptResults[-1] if direction is not DIRECTION.BACKWARD else self.get_next_image_folder(imagePromptResults[-1], currentTimePromptDirectories, sortedDatesDirectory, direction)[0]
                if(directoryToTokenize is not None):
                    nextToken = NextToken(
                        prompt=directoryToTokenize.prompt,
                        repo=self.imageRepo,
                        date=directoryToTokenize.date,
                        time=directoryToTokenize.time
                    )
            return nextToken

        for num in range(0, number):
            try:
                promptWithTime = self.generate_file_name(currentDirectory.time, currentDirectory.prompt)

                logging.debug(f"Getting files for {currentDirectory.date} and {promptWithTime}")

                # if going backwards the token provided will be within the next page. As such include it. There are also scenarios (first initialization) where a caller needs to force include a forward direciton call too
                if(num == 0 and (direction is DIRECTION.BACKWARD or forceIncludeCurrentDirectoryInResults)):
                    nextImageFolder = currentDirectory
                    logging.debug(f"Including current directory in results")
                else:
                    nextImageFolder, currentTimePromptDirectories = self.get_next_image_folder(currentDirectory, currentTimePromptDirectories, sortedDatesDirectory, direction)

                if(nextImageFolder is not None):
                    promptWithTime = self.generate_file_name(nextImageFolder.time, nextImageFolder.prompt)
                    imagePromptResults.append(self.get_files(date=nextImageFolder.date, folderName=promptWithTime))
                    currentDirectory = nextImageFolder
                else:
                    break
            except BaseException as e:
                logging.warning(e)
                break

        resultNextToken = generate_nextToken(imagePromptResults)

        # Order the page worth of data as though the direction was forward rather then backward
        if direction is DIRECTION.BACKWARD:
            imagePromptResults.reverse()

        return GetImagePrompsResult(
            imagePromptResults, 
            resultNextToken
        )


    def get_images_background(self, number: int, token: NextToken, includeCurrentDirectoryInResults: bool = False) -> GetImagePrompsResult:
        logging.info("Getting backwards images")
        currentPrompt = token.prompt
        currentImageDate = token.date
        currentImageTime = token.time

        imagePromptResults: List[ImagePrompResult] = []

        sortedDatesDirectory = get_sorted_directory_by_name(self.imageRepo)
        currentTimePromptDirectories = get_sorted_directory_by_name(self.imageRepo/currentImageDate)

        for num in range(0, number):
            try:
                promptWithTime = self.generate_file_name(currentImageTime, currentPrompt)

                imagePromptResults.append(self.get_files(date=currentImageDate, prompt_time=promptWithTime))

                nextImageIndex = currentTimePromptDirectories.index(promptWithTime) - 1
                if(nextImageIndex >= 0):
                    currentImageFolder = currentTimePromptDirectories[nextImageIndex]
                    currentImageTime, currentPrompt = currentImageFolder.split("_")
                else:
                    # go to the next date as this directory is exhausted
                    nextDateIndex = sortedDatesDirectory.index(currentImageDate) - 1
                    currentImageDate = sortedDatesDirectory[nextDateIndex]
                    currentTimePromptDirectories = get_sorted_directory_by_name(self.imageRepo/currentImageDate)
                    currentImageTime, currentPrompt = currentTimePromptDirectories[0].split("_")

            except BaseException as e:
                logging.warning(e)
                break

        return GetImagePrompsResult(
            imagePromptResults, 
            NextToken(
                prompt=imagePromptResults[0].prompt,
                repo=self.imageRepo,
                date=imagePromptResults[0].date,
                time=imagePromptResults[0].time
            )
        )


    def save_image(self, prompt: str, image: Image) -> ImagePrompResult:
        directoryResult = self.generate_png_path(prompt)
        image.save(directoryResult.absolutePath, "PNG")
        return ImagePrompResult(
            prompt = directoryResult.prompt,
            repo = directoryResult.repo,
            date = directoryResult.date,
            time = directoryResult.time,
            num = 1,
            pngPaths = [directoryResult.absolutePath/"1.png"]
        )
