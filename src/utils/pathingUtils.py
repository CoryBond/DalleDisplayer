from enum import Enum
from pathlib import Path
import os
from typing import List

from utils.algoUtils import reverse_bisect_left, reverse_bisect_right


RESOURCES_FOLDER = 'resources'


class DIRECTION(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"


def get_project_root() -> Path:
    """
    Gets the absolute path of the PAIID project.
    """
    return Path(__file__).parent.parent


def get_resources(resourcesFolder: str = RESOURCES_FOLDER) -> Path:
    image_repo_path = get_project_root()/'..'/resourcesFolder
    return image_repo_path


def get_or_create_resources(resourcesFolder: str = RESOURCES_FOLDER) -> Path:
    image_repo_path = get_resources(resourcesFolder)
    image_repo_path.mkdir( parents=True, exist_ok=True )
    return image_repo_path


def get_image_repos(resourcesFolder: str = RESOURCES_FOLDER) -> Path:
    image_repo_path = get_or_create_resources(resourcesFolder)/'imageRepos'
    return image_repo_path


def get_or_create_image_repos(resourcesFolder: str = RESOURCES_FOLDER) -> Path:
    image_repo_path = get_image_repos(resourcesFolder)
    image_repo_path.mkdir( parents=True, exist_ok=True )
    return image_repo_path


def get_or_create_log_directory(resourcesFolder: str = RESOURCES_FOLDER) -> Path:
    log_path = get_or_create_resources(resourcesFolder)/'logs'
    log_path.mkdir( parents=True, exist_ok=True )
    return log_path
    

def get_or_create_image_resources(resourcesFolder: str = RESOURCES_FOLDER) -> Path:
    image_resources_path = get_or_create_resources(resourcesFolder)/'images'
    image_resources_path.mkdir( parents=True, exist_ok=True )
    return image_resources_path
    

def get_sorted_directory_by_name(path: Path, reverse: bool) -> List[str]:
    """
    Gets all directories and files from the file system from the proivded directory path in sorted order.

    Parameters
    ----------
    path: (Path):
        The path to get directories/files from
    
    reverse: bool:
        Whether to sort in reverse or not. Defaults to false.

    Returns
    -------
    List[str]
        All directories and files by name. Results will be sorted by their file/directory name.

    """
    def get_name(entry):
        return entry.name

    with os.scandir(path) as entries:
        sorted_entries = sorted(entries, key=get_name, reverse=reverse)
        sorted_items = [get_name(entry) for entry in sorted_entries]
    return sorted_items


def get_reverse_sorted_directory_by_name(directory: Path) -> List[str]:
    """
    Same as get_sorted_directory_by_name but in reverse order.
    """
    return get_sorted_directory_by_name(directory, reverse=True)


def get_next_file_index_from_reverse_sorted(fileName: str, reverseSortedFiles: List[str], direction: DIRECTION = DIRECTION.FORWARD) -> int:
    """
    Util function that gets the next logical index of a given file in a sorted file list. If the provided file has no "next" entry
    then None is retruned instead
    

    The performance of this function should be Olog(s = size of reverseSortedFiles) for getting the next index.

    NOTE: Maybe worth converting this to a more generic "algo" util function and drop the file aestestics surronding it.
          This function could be used in othere scenarios that aren't related to files but sorted string lists in general.

    Parameters
    ----------
    fileName: (str):
        The file name to search the sorted files in.

    reverseSortedFiles: (list):
        The files to search the files next index in.
        The provided list of files must be sorted IN REVERSE order for this function to work properly.

    Returns
    -------
    int
        A number if there exists a next logical entry for the provided file or None if not
    """
    if(reverseSortedFiles is not None and len(reverseSortedFiles) > 0):
        if(direction is not DIRECTION.BACKWARD):
            nextIndex = reverse_bisect_right(reverseSortedFiles, fileName)
            if(nextIndex < len(reverseSortedFiles)):
                return nextIndex
        else:
            nextIndex = reverse_bisect_left(reverseSortedFiles, fileName)
            if(nextIndex != 0):
                return nextIndex - 1
    return None