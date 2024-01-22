import logging
import os
from pathlib import Path
from typing import Union
from repoManager.Models import ImagePromptDirectory
from repoManager.utils import generate_file_name

from utils.pathingUtils import get_reverse_sorted_directory_by_name, get_next_file_index_from_reverse_sorted, DIRECTION


class DirectoryIterator:
    """
    An iterator that simplifies traversal of the file system. Its primary mode of traversal is going to the logical "next"
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
    systems hash system. For optimization purposes that is why a "snapshot" of the dates is used to reduce having to
    sort all dates when loading them from the file system.

    The DirectoryIterator has internal pionters to where it is in the directory structure. These pointers start
    at the very first entry in the directory structure depending on the direction provided (default of Forward.) These 
    pointers can be adjusted with a provided startingDirectory arg. The startingDirectory does not need to be physical
    directory in the system aand this DirectoryIterator will iterate to the next logical entry of the provided starting directory
    if that is the case.
    
    """
    def __init__(self, pathToDirectories: Union[str, Path], startingDirectory: ImagePromptDirectory = None, direction: DIRECTION = DIRECTION.FORWARD):
        self.pathToDirectories = Path(pathToDirectories)
        self.sortedDateDirectories = get_reverse_sorted_directory_by_name(self.pathToDirectories)

        if(startingDirectory is not None):
            # if directory provided (even if it doesn't exist) use that
            startingPromptWithTime = generate_file_name(startingDirectory.time, startingDirectory.prompt)
            self.currentDate = startingDirectory.date
            self.currentTimePromptDirectories = get_reverse_sorted_directory_by_name(self.pathToDirectories/self.currentDate)
            self.currentTimePrompt = startingPromptWithTime
        else:
            # Otherwise set to the first entry
            if(direction is DIRECTION.BACKWARD):
                self._rewind_to_backward()
            else:
                self._rewind_to_forward()


    def _rewind_to_forward(self):
        self.currentDate = "9999-99-99" # I would be blessed if I lived to see this be an error
        self.currentTimePromptDirectories = []
        self.currentTimePrompt = ""
        self.get_next_time_prompt_directories(direction = DIRECTION.FORWARD)


    def _rewind_to_backward(self):
        self.currentDate = "0000-00-00"
        self.currentTimePromptDirectories = []
        self.currentTimePrompt = ""
        self.get_next_time_prompt_directories(direction = DIRECTION.BACKWARD)


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
            time, prompt = self.currentTimePrompt.split("_")
            return ImagePromptDirectory(
                prompt=prompt,
                time=time,
                # Get only the repo name. Not the full absolute path of the repo.
                repo=os.path.basename(os.path.normpath(self.pathToDirectories)),
                date=self.currentDate,
            )
        return None


    def _iterate_time_prompt(self, direction: DIRECTION = DIRECTION.FORWARD) -> ImagePromptDirectory:
        # attempt to get next time prompt within current date directory
        nextTimePromptIndex = get_next_file_index_from_reverse_sorted(fileName=self.currentTimePrompt, reverseSortedFiles=self.currentTimePromptDirectories, direction=direction)
        if(nextTimePromptIndex is not None):
            nextTimePrompt = self.currentTimePromptDirectories[nextTimePromptIndex]
            self.currentTimePrompt = nextTimePrompt
            return self.get_current_image_prompt_directory()
        self.currentTimePrompt = None   
        return None


    def _iterate_date(self, direction: DIRECTION = DIRECTION.FORWARD) -> ImagePromptDirectory:
        # attempt to get next time prompt within current date directory
        nextDateIndex = get_next_file_index_from_reverse_sorted(fileName=self.currentDate, reverseSortedFiles=self.sortedDateDirectories, direction=direction)

        if(nextDateIndex is not None):
            nextDate = self.sortedDateDirectories[nextDateIndex]
            nextTimePromptDirectories = get_reverse_sorted_directory_by_name(self.pathToDirectories/nextDate)

            startIndexOfNextDateFolder = 0 if direction is not DIRECTION.BACKWARD else len(nextTimePromptDirectories)-1
            nextTimePrompt = nextTimePromptDirectories[startIndexOfNextDateFolder]

            self.currentDate = nextDate
            self.currentTimePromptDirectories = nextTimePromptDirectories
            self.currentTimePrompt = nextTimePrompt   
            return self.get_current_image_prompt_directory()
        self.currentDate = None
        self.currentTimePromptDirectories = None
        self.currentTimePrompt = None   
        return None 


    def get_next_time_prompt_directories(self, direction: DIRECTION = DIRECTION.FORWARD) -> ImagePromptDirectory:
        """
        Gets the logical next image prompt that this iterator from the current image prompt this iterator is
        pointing to. It could also return None if all image prompts have been exhuasted.

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
        logging.debug(f'Getting next prompt with direction {direction}')

        # get next time prompt if current date direcotry has any
        candidate_time_prompt_directory = self._iterate_time_prompt(direction)

        # Iterate through date directories until a time prompt directory is found or all date directories are exhuasted
        while(self.currentDate is not None and candidate_time_prompt_directory is None):
            candidate_time_prompt_directory = self._iterate_date(direction)
        
        return candidate_time_prompt_directory 