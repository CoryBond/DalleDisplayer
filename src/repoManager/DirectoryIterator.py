import logging
import os
from pathlib import Path
from typing import Union, List
from repoManager.Models import ImagePromptDirectory
from repoManager.utils import generate_file_name, extract_file_name

from utils.pathingUtils import get_reverse_sorted_directory_by_name
from utils.algoUtils import get_next_string_index_from_reverse_sorted
from utils.enums import DIRECTION


def get_start_index(direction: DIRECTION, collection: List):
    return 0 if direction is not DIRECTION.BACKWARD else len(collection)-1


def get_before_start_index(direction: DIRECTION, collection: List):
    return -1 if direction is not DIRECTION.BACKWARD else len(collection)


class DirectoryIterator:
    """
    An iterator that simplifies traversal of the file system for an image repo. Its primary mode of traversal is going to the logical "next"
    prompt directory in the system.

    When created the DirectoryIterator first makes a snapshot of the date directories and orders them by most recent. This snapshot
    can become stale so users of this Directory Iterator should make a new Directory Iterator to get a more recent snapshot
    of dates.

    Logically the repo directory structure can look as follows:
        ${pathToDirectories}/
            2024-01-11/
                15:05:06.713451_Sad rat/
                    1.png
                    2.png
                16:55:31.897695_Mom yelling/
                    1.png

    Whatever the "pathToDirectories" location is there will be directories there named by iso-8601 date format.
    Within each directory a prompt, prefixed by the iso-8601 time used to generated it, exists.
    Within each timePrompt directory the images generated for that prompt are stored.

    When saved to the file system the actual directories won't be sorted, as they are actual stored by order of the file
    systems hash. For optimization purposes that is why a "snapshot" of the dates are used to reduce re-sorting all dates 
    for every next call.

    The DirectoryIterator has internal pointers to where it is in the directory structure. These pointers can be adjusted with a 
    provided startingDirectory arg. The startingDirectory does not need to be physical directory in the system and this 
    DirectoryIterator will iterate to the next logical entry from the provided starting directory.
    
    """
    def __init__(self, pathToDirectories: Union[str, Path], startingDirectory: ImagePromptDirectory = None, direction: DIRECTION = DIRECTION.FORWARD):
        self.pathToDirectories = Path(pathToDirectories)
        self.sortedDateDirectories = get_reverse_sorted_directory_by_name(self.pathToDirectories)
        self.direction = direction

        if(startingDirectory is not None):
            # if directory provided (even if it doesn't exist) use that
            startingPromptWithTime = generate_file_name(startingDirectory.time, startingDirectory.prompt)
            self.currentDate = startingDirectory.date
            self.dateIndex = None
            timePromptPath = self.pathToDirectories/self.currentDate
            self.currentTimePromptDirectories = get_reverse_sorted_directory_by_name(timePromptPath) if timePromptPath.exists() else []
            self.currentTimePrompt = startingPromptWithTime
            self.timePromptIndex = None
        else:
            self.currentDate = None
            self.dateIndex = get_before_start_index(self.direction,  self.sortedDateDirectories)
            self.currentTimePromptDirectories = []
            self.currentTimePrompt = None
            self.timePromptIndex = get_before_start_index(self.direction, self.currentTimePromptDirectories)


    def __iter__(self):
        return self


    def get_current_image_prompt_directory(self) -> ImagePromptDirectory:
        """
        Gets the current image prompt that this iterator is pointing to. 

        Returns
        -------
        ImagePromptDirectory
            A directory model that could represent a physical entry. However the physical entry 
            could of been deleted externally since the last time this iterator took a snapshot of the time_prompts 
            directories for a given date.

        """
        logging.debug(f'Getting the current directory')
        if(
            self.currentTimePrompt is not None and
            self.pathToDirectories is not None and
            self.currentDate is not None
           ):
            time, prompt = extract_file_name(self.currentTimePrompt) # split only the first instance!
            dir = ImagePromptDirectory(
                prompt=prompt,
                time=time,
                # Get only the repo name. Not the full absolute path of the repo.
                repo=os.path.basename(os.path.normpath(self.pathToDirectories)),
                date=self.currentDate,
            )
            logging.info(f'Time Prompt Directory Found {dir}')
            return dir
        return None


    def _iterate_time_prompt(self) -> ImagePromptDirectory:
        logging.debug(f'Iterating To Next Time Prompt')

        # attempt to get next time prompt within current date directory
        # Either
        # 1. Get next index from existing index
        # 2. Find next index from current time prompt
        nextTimePromptIndex = None
        if(self.timePromptIndex is None):
            nextTimePromptIndex = get_next_string_index_from_reverse_sorted(theString=self.currentTimePrompt, reverseSortedStrings=self.currentTimePromptDirectories, direction=self.direction)
        elif (self.direction is DIRECTION.FORWARD and self.timePromptIndex < len(self.currentTimePromptDirectories)-1):
            nextTimePromptIndex = self.timePromptIndex + 1 
        elif (self.direction is DIRECTION.BACKWARD and self.timePromptIndex > 0):
            nextTimePromptIndex = self.timePromptIndex - 1

        # attempt to get next time prompt within current date directory
        if(nextTimePromptIndex is not None):
            nextTimePrompt = self.currentTimePromptDirectories[nextTimePromptIndex]
            self.currentTimePrompt = nextTimePrompt
            self.timePromptIndex = nextTimePromptIndex
            return self.get_current_image_prompt_directory()
        logging.debug(f'TimePrompts exhuasted under date')
        self.currentTimePrompt = None   
        self.timePromptIndex = None
        return None


    def _iterate_date(self) -> ImagePromptDirectory:
        logging.debug(f'Iterating To Next Date')
        # attempt to get next time prompt within current date directory
        # Either
        # 1. Get next index from existing index
        # 2. Find next index from current date
        nextDateIndex = None
        if(self.dateIndex is None):
            nextDateIndex =  get_next_string_index_from_reverse_sorted(theString=self.currentDate, reverseSortedStrings=self.sortedDateDirectories, direction=self.direction)
        elif (self.direction is DIRECTION.FORWARD and self.dateIndex < len(self.sortedDateDirectories)-1):
            nextDateIndex = self.dateIndex + 1
        elif (self.direction is DIRECTION.BACKWARD and self.dateIndex > 0):
            nextDateIndex = self.dateIndex - 1

        if(nextDateIndex is not None):
            nextDate = self.sortedDateDirectories[nextDateIndex]
            logging.debug(f'Looking at date {nextDate}')
            nextTimePromptDirectories = get_reverse_sorted_directory_by_name(self.pathToDirectories/nextDate)

            startIndexOfNextDateFolder = get_start_index(self.direction,  nextTimePromptDirectories)
            nextTimePrompt = nextTimePromptDirectories[startIndexOfNextDateFolder]

            self.currentDate = nextDate
            self.dateIndex = nextDateIndex
            self.currentTimePromptDirectories = nextTimePromptDirectories
            self.currentTimePrompt = nextTimePrompt   
            self.timePromptIndex = startIndexOfNextDateFolder
            return self.get_current_image_prompt_directory()
        logging.debug(f'Dates exhausted')
        self.dateIndex = None
        self.currentDate = None
        self.currentTimePromptDirectories = None
        self.currentTimePrompt = None   
        self.timePromptIndex = None
        return None 


    def _exhuasted_all_dates(self):
        return self.currentDate is None and self.dateIndex is None


    def __next__(self) -> ImagePromptDirectory:
        """
        Gets the next logical image prompt from previous iterations on this iterator.

        Not garanteed to be 100% accurate in scenarios where the physical file system has been externally
        modified.

        Parameters
        ----------
        direction: (DIRECTION):
            The direciton to get the next prompt time directory. Supports "forward" or "backward". 
            Default is to go forward.

        Returns
        -------
        ImagePromptDirectory
            A directory model that could represent the next logical physical entry. However the physical entry 
            could of been deleted externally since the last time this iterator took a snapshot of the time_prompts 
            directories for a given date.

        """
        if(self._exhuasted_all_dates()):
            raise StopIteration
        
        logging.debug(msg=f'Getting next prompt with direction {self.direction}')

        # get next time prompt if current date direcotry has any
        candidate_time_prompt_directory = self._iterate_time_prompt()

        # Iterate through date directories until a time prompt directory is found or all date directories are exhuasted
        while(candidate_time_prompt_directory is None and not self._exhuasted_all_dates()):
            candidate_time_prompt_directory = self._iterate_date()

        if(self._exhuasted_all_dates()):
            raise StopIteration
        
        return candidate_time_prompt_directory 