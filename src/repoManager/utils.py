
def generate_file_name(time: str, prompt: str):
    """
    Generates a file name where the time is concated by the prompt.

    Storing prompts with a time prefix allows for sorting the prompts by
    most recent time they were generated.
    """
    return time + "_" + prompt