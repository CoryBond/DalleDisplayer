from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_image_repos() -> Path:
    return get_project_root()/'..'/'resources'/'imageRepos'