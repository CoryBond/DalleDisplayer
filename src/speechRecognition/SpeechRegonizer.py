from typing import Callable


class SpeechRecognizer(object):
    """
    Interface that defines the API for transcriptions from real input audio to text 

    Transcriptions all run in a background thread as to not halt the main thread. This is particularly important
    in GUIs with an event loop as simply using asynchronous (asyncio) functions can still hang the main thread from rendering items.

    Any class implementing this interface assumes a few things:
    1. Multiple transcription sessions can not happen at the same time with the same input source (like a microphone)
    2. Transcriptions run in a background thread and stop when they are called to stop

    Attributes
    ----------

    Methods
    ----------
    get_transcription()
        Retrieves the current transcription that the recognizer was able to translate from audio so far

    transcribe(notify) -> Callable
        Runs a background thread that collects audio, converts it to text and adds to an ongoing transcription. 
        "notify" is called whenever parts of the audio were added to the existing transcription.
        Will stop when the callback returned by this function is called.
    """

    def __init__(self):
        return
    
    
    def get_transcription(self) -> str:
        return


    def transcribe(self, notify: Callable = None) -> Callable:
        return