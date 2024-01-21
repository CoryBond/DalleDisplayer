from pathlib import Path
import os
from typing import List


def get_project_root() -> Path:
    """
    Gets the absolute path of the PAIID project.
    """
    return Path(__file__).parent.parent


def get_or_create_image_repos() -> Path:
    image_repo_path = get_project_root()/'..'/'resources'/'imageRepos'
    image_repo_path.mkdir( parents=True, exist_ok=True )
    return image_repo_path


def get_or_create_log_directory() -> Path:
    log_path = get_project_root()/'..'/'resources'/'logs'
    log_path.mkdir( parents=True, exist_ok=True )
    return log_path
    

def get_or_create_image_resources() -> Path:
    image_resources_path = get_project_root()/'..'/'resources'/'images'
    image_resources_path.mkdir( parents=True, exist_ok=True )
    return image_resources_path
    

def get_sorted_directory_by_name(directory: Path) -> List[str]:
    """
    Not as efficient as getting directory by created time
    """
    def get_name(entry):
        return entry.name

    with os.scandir(directory) as entries:
        sorted_entries = sorted(entries, key=get_name, reverse=True)
        sorted_items = [get_name(entry) for entry in sorted_entries]
    return sorted_items