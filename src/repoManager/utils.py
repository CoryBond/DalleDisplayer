from repoManager.Models import ImagePromptDirectory
from pathlib import Path


def extract_file_name(timePrompt: str):
    """
    Extracts the time and prompt from a timeprompt name
    """
    return timePrompt.split("_", 1) # split only the first instance!


def generate_file_name(time: str, prompt: str):
    """
    Generates a file name where the time is concated by the prompt.

    Storing prompts with a time prefix allows for sorting the prompts by
    most recent time they were generated.
    """
    return time + "_" + prompt


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