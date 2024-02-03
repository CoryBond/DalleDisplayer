from typing import Union, Dict, List
import os
from pathlib import Path
from pyfakefs.fake_filesystem import FakeFilesystem 
from utils.pathingUtils import get_project_root


TimeWithPromptDictType = Dict[str, List[str]]
DateDictType = Dict[str, TimeWithPromptDictType]


def populate_fs_with(fs: FakeFilesystem, path: Union[Path, str], dateDictStructure : DateDictType):
    """
    Simulates a files and folders in a fake file system when accessing the images repo.

    Will populate the fake file system with:

    * Dates folder
    * The TimePrompts of a date folder if the absolute date path is passed in
    * Images per TimePrompts
    """
    path = Path(path)
    if(not os.path.exists(path)): # I know no other way with FakeFilesystem to first check if dirctory exists first.
        fs.create_dir(path) # Does not support  exist_ok=True flag like makedirs does :/
    for date, timePrompts in dateDictStructure.items():
        fs.create_dir(path/date)
        for timePrompt, images in timePrompts.items():
            fs.create_dir(directory_path=path/date/timePrompt)
            for image in images:
                # Use a real image to simplify the test
                fs.add_real_file(source_path=get_project_root()/'..'/'testResources'/'images'/'ai'/"test1.png", target_path=path/date/timePrompt/image)