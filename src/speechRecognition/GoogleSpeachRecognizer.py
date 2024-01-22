import logging
import traceback
from speech_recognition import Recognizer, UnknownValueError, RequestError, Microphone
import logging
from typing import Callable

from speechRecognition.SpeechRegonizer import SpeechRecognizer


class GoogleSpeechRecognizer(SpeechRecognizer):
    """
    Class that implements the SpeechRecognizer interface using the google audio API.

    Right now this class uses the default API key when using Google's Audio Transcription service.
    See : https://cloud.google.com/speech-to-text

    Important notes about the default API Key:
    1. It is free
    2. All customers get 60 minutes per month to use it

    Right now there is no way to configure this class to use any other API key so it is stuck the service limitations
    of the default API key.
    """

    def __init__(self):
        super().__init__()
        # Initialize the recognizer 
        self.r = Recognizer()
        self.trascription = ""
        return


    def get_transcription(self) -> str:
        return self.trascription


    def transcribe(self, notify: Callable = None) -> Callable:
        self.trascription = ""
        try:
            # this is called from the background thread
            def callback(recognizer: Recognizer, audio):
                # received audio data, now we'll recognize it using Google Speech Recognition
                try:
                    # for testing purposes, we're just using the default API key
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    innertext = recognizer.recognize_google(audio)
                    logging.info("Google Speech Recognition thinks you said " + innertext)
                    self.trascription += " " + innertext

                    # Notify any callers who want updates on transcription changes
                    if notify:
                        notify()
                except UnknownValueError:
                    logging.warn("Google Speech Recognition could not understand audio")
                except RequestError as e:
                    logging.error("Could not request results from Google Speech Recognition service; {0}".format(traceback.format_exc()))

            # use the microphone as source for input.
            mic = Microphone()
            with mic as source:
                logging.info("Listening To Mic Input")
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                self.r.adjust_for_ambient_noise(source)

            #listens for the user's input 
            return self.r.listen_in_background(mic, callback)
                
        except RequestError as e:
            logging.info("Could not request results; {0}".format(e))
            
        except UnknownValueError:
            logging.info("unknown error occurred")