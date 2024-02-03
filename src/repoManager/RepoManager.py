import logging
import traceback
import os
from pathlib import Path
from typing import Union, List
from repoManager.DirectoryIterator import DirectoryIterator
from repoManager.Models import ImagePrompResult, NextToken, ImagePromptDirectory, GetImagePrompsResult

from repoManager.utils import generate_file_name
from utils.dateUtils import generate_ios_date_time_strs
from PIL import Image

from utils.pathingUtils import DIRECTION


def generate_nextToken(directoryToTokenize: ImagePromptDirectory):
    """
    Takes an image prompt directory and generates a token for it. Tokens are uesd in pagination systems
    to bookmark what page a client was last at when getting items.

    For the repo manager a token is basically just a image prompt directory. This doesn't have to be the
    case though. In fact for clients, the actual implementation of the token shouldn't be important for
    most interactions with the repo manager. The only thing the client has to do is provide previous nexttokens
    in order to get the next page of imageprompt directories from the system.

    Parameters
    ----------
    directoryToTokenize (ImagePromptDirectory): 
        Model of a image prompt directory that will be tokenized

    Returns
    -------
    NextToken
        The nexttoken used for pagination and bookmarking.

    """
    nextToken = None
    if(directoryToTokenize is not None):
        nextToken = NextToken(
            prompt=directoryToTokenize.prompt,
            repo=directoryToTokenize.repo,
            date=directoryToTokenize.date,
            time=directoryToTokenize.time
        )
    return nextToken


def generate_image_prompt_path(directory: ImagePromptDirectory) -> Path:
    """
    Converts a directory model into a file system path

    Parameters
    ----------
    directory (ImagePromptDirectory): 
        Model representing the directory within the image repo.

    Returns
    -------
    Path
        Path representing the file system location the image prompt directory modelled.
        Can be used to do filesystem operations on the directory.
    
    """
    return Path(directory.repo)/directory.date/generate_file_name(directory.time, directory.prompt)


class RepoManager(object):
    """
    Class that manages a colleciton of AI image repositories set in a local file system.

    AI Image repos are saved per repo under the provided reposPath arg. Within each repo, images
    are partitioned by date first. Per date the images are saved together under the prompt and time they were generated.
    So, for example, if we have a prompt "Sad rat" which generated 2 images then they can be potentially saved under the path
    "$reposPath/Dall-e/2024-01-11/15:05:06.713451_Sad rat" as "1.png" and "2.png"

    The repo manager will attempt to make a folder of the provided reposPath if it doesn't already exist. If the Repo Manager
    cannot make the provided reposPath for any reason it will throw an exception.

    Accessing images supports pagination.

    NOTE: Currently the "images" returned by this repo manager are actually paths to the image on the file system. Clients are expected to
    access the file system if they want to actually get the images. This was a early design that simplified the implementation without
    having to fluff with byte conversions in testing. The repo manager and its clients were never expected to be used outside the same 
    filesystem. A better, less coupled design would have the Repo Manager return the actual images themselves (as bytes). Maybe a 
    design improvement for future iterations.    
    """

    def __init__(self, reposPath: Union[str, Path], startingRepo: str):
        self.reposPath = Path(reposPath)
        os.makedirs(self.reposPath, exist_ok=True)
        self.switch_repo(startingRepo)


    def current_repo(self) -> str:
        return self.imageRepo.name


    def current_repo_abs_path(self) -> Path:
        return self.reposPath/self.current_repo()


    def switch_repo(self, newRepo: str):
        """
        Changes the repo folder for the manager. 
        Older tokens for the previous repo should be discarded if repos change.

        Parameters
        ----------
        newRepo (str): 
            The new repo folder the repo manager will use for all operations.
            The repo manager will not create a directory on the file system for this repo until the repo manager needs
            to save something to it.
        """
        self.imageRepo: Path = self.reposPath/newRepo
        os.makedirs(self.imageRepo, exist_ok=True)


    def generate_image_prompt_directory(self, prompt: str) -> [ImagePromptDirectory, str]:
        """
        Take the given prompt and generate a date/time-prompt entry within the given repo directory.
        Will use the current date and time this method was called to generate the directory.

        Will atempt to create the entries absolute path of the entry if fs permissions allow it. This 
        should be safe as RepoManager will error out 

        Parameters
        ----------
        prompt (str): 
            the prompt to generate an repo entry for

        Returns
        -------
        ImagePromptDirectory
            A model representing the newly generate image prompt directory.
        
        """
        date, time = generate_ios_date_time_strs()
        dayDirectory = self.imageRepo/date

        promptWithTime = generate_file_name(time, prompt)
        promptAbsPath = dayDirectory/promptWithTime
        promptAbsPath.mkdir( parents=True, exist_ok=True )

        return [
            ImagePromptDirectory(
                prompt,
                repo=self.current_repo(),
                date=date,
                time=time
            ), 
            promptAbsPath
        ]


    def _generate_abs_image_prompt_path(self, directory: ImagePromptDirectory):
        directorySubPath = generate_image_prompt_path(directory)
        return self.reposPath/directorySubPath


    def _get_files(self, directory: ImagePromptDirectory) -> ImagePrompResult:
        logging.info(f"Attempting to load images from path {self.reposPath} and directory {directory}")
        fullPathToImagePromptFolder = self._generate_abs_image_prompt_path(directory)

        fullImagePaths = [fullPathToImagePromptFolder/img_file for img_file in os.listdir(fullPathToImagePromptFolder)]

        logging.info(f"Found {len(fullImagePaths)} images")
        logging.debug(f"Found the images : {str(fullImagePaths)}")
        return ImagePrompResult(
            prompt=directory.prompt,
            repo=directory.repo,
            date=directory.date,
            time=directory.time,
            num="1",
            pngPaths=fullImagePaths
        )


    def get_latest_images_in_repo(self) -> ImagePrompResult:
        """
        Gets the very first prompt_time images from the repo if possible.
        Unlike other paginated access functions this method will return None
        at any point there is a exception.

        Returns
        -------
        ImagePrompResult
            A API result containing the images and other meta data of the images.
        
        """
        logging.info("Attempting to load last image created")
        try:
            return self.get_images(number = 1).results[0]
        except:
            return None


    def get_images(self, number: int, token: NextToken = None, direction: DIRECTION = DIRECTION.FORWARD) -> GetImagePrompsResult:
        """
        Pagination call to get prompts and their images from the repo. Results will be returned in order by the most recent date 
        and time.
        
        If there are less items avaialble then requested then those entries will be returned in full instead of the requested number.
        The results returned will contain the prompts, their metadata and all existing images created by the prompt. 

        Any intenal exceptions will be caught and returned as a response with whatever results were collected up to that point if
        possible.

        Pagination is supported via a token system. A token represents a bookmark which, when provided in subsequent calls,
        will then return results starting from the bookmark. Implementation-wise the token is:
        1. None if no more entries could of been retrieved
        2. For forward requests the last entry from the page
        3. For backwards requests the FIRST entry from the next page (if possible)
        This design allows for a sliding window approach to pagination where clients can store a "left" and a "right" token
        which they can use to go back or forward across pages.
        Tokens do not have to represent a real prompt entry in the file system (in scenarios where the entry was deleted after the
        token was generated) and if provided these tokens will still get the next logical pages worth of resutls as though the token
        did represent a physical entry.

        Parameters
        ----------
        number (int):
            The number of prompts to get images from to get. It does NOT represent how many images to get.

        token: (NextToken):
            An optional token that bookmarks and gets results starting from that bookmark point

        direction: (DIRECTION):
            The direciton to get page results from. Supports "forward" or "backward". Default is to go forward.

        Returns
        -------
        GetImagePrompsResult
            A model representing the results of prompts, their images, or optionally error messages.
            Also contains a nextToken if getting images is not exhuasted.
            Results are sorted by most recent date then most recent time. 

        """
        try:
            logging.debug(f"Provided token : {token}")
            return self._get_images(number, startingDirectory=token, direction=direction)
        except BaseException as e:
            logging.error(traceback.format_exc())
            return GetImagePrompsResult(
                results=[],
                errorMessage = f'Critical error retrieving any results : {str(e)}',
            )


    def _directory_exists(self, directory: ImagePromptDirectory):
        return directory is not None and os.path.exists(self._generate_abs_image_prompt_path(directory))


    def _get_images(self, number: int, startingDirectory: ImagePromptDirectory = None, direction: DIRECTION = DIRECTION.FORWARD) -> GetImagePrompsResult:
        logging.info(msg="Getting images")
        if(number < 1):
            return GetImagePrompsResult(results=[], errorMessage="Number must be greater then 0")

        imagePromptResults: List[ImagePrompResult] = []
        errorMessage = None

        try:
            directoryIterator = DirectoryIterator(pathToDirectories=self.imageRepo, startingDirectory=startingDirectory, direction=direction)

            # If going backwards add the current directory but only if it actually exists. Otherwise continue iterating from the start directory.
            if(direction is DIRECTION.BACKWARD and self._directory_exists(startingDirectory)):
                imagePromptResults.append(self._get_files(directory=startingDirectory))

            # Iterate prompt directories until either we found enough prompt directories to match the number requested or until there are none left in the direction we are iterating
            for _ in range(len(imagePromptResults), number):
                # if going backwards the token provided will be within the next page. As such include it. There are also scenarios (first initialization) where a caller needs to force include a forward direciton call too
                nextTimeWithPromptDirectory = next(directoryIterator)

                # if 
                if(nextTimeWithPromptDirectory is not None):
                    imagePromptResults.append(self._get_files(directory=nextTimeWithPromptDirectory))
                else:
                    break

        except BaseException as e:
            logging.error(traceback.format_exc())
            errorMessage = f'Critical error while retrieving results : {str(e)}'
        finally:
            nextToken = None
            # Order the page worth of data as though the direction was forward rather then backward
            if direction is DIRECTION.BACKWARD:
                imagePromptResults.reverse()
                nextToken= generate_nextToken(next(directoryIterator))
            else:
                nextToken = generate_nextToken(directoryIterator.get_current_image_prompt_directory())

            return GetImagePrompsResult(
                imagePromptResults, 
                nextToken=nextToken,
                errorMessage=errorMessage,
            )
    

    def save_image(self, prompt: str, image: Image) -> ImagePrompResult:
        """
        Method to save images and their associated prompt to the file system. Images will be stored and indexed by the
        date and time in which they were saved. Additionally the image will be saved to whatever repo this repo manager
        is currently set to.

        Parameters
        ----------
        prompt (str):
            The prompt used to save the image

        image: (Image):
            The actual image to be saved

        Returns
        -------
        ImagePrompResult
            The meta information after the image was saved.
        """
        directoryResult, absolutePath = self.generate_image_prompt_directory(prompt)

        try:
            image.save(absolutePath/"1.png", "PNG")
            logging.info(f'Saved {absolutePath/"1.png"}')
        except BaseException as e:
            # In scenarios where the Pillow libraries encoder doesn't work 
            # (fake filesystem issues : https://github.com/pytest-dev/pyfakefs/discussions/858)
            # attempt to save the file via native os API
            with open(absolutePath/"1.png", 'wb') as f:
                f.write(image.tobytes())
                logging.info(f'Saved {absolutePath/"1.png"}')

        return ImagePrompResult(
            prompt = directoryResult.prompt,
            repo = directoryResult.repo,
            date = directoryResult.date,
            time = directoryResult.time,
            num = 1,
            pngPaths = [absolutePath/"1.png"]
        )
