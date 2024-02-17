from pathlib import Path
import os
from typing import List


RESOURCES_FOLDER = 'resources'


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
    

def read_file_as_bytes(file_path: Path) -> bytes:
    """
    Takes a files path and reads it as bytes
    """
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    return file_bytes


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
