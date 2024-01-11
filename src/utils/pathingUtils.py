from pathlib import Path


def get_project_root() -> Path:
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
    