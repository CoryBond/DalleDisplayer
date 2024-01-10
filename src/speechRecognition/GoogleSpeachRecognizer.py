
# Python program to translate
# speech to text and text to speech
 
import logging
import speech_recognition as sr
import logging
from typing import Callable

from speechRecognition.SpeechRegonizer import SpeechRecognizer


class GoogleSpeechRecognizer(SpeechRecognizer):


    def __init__(self):
        super().__init__()
        # Initialize the recognizer 
        self.r = sr.Recognizer()
        self.trascription = ""
        return


    def get_transcription(self) -> str:
        return self.trascription


    def transcribe(self, notify: Callable = None) -> Callable:
        self.trascription = ""
        try:
            # this is called from the background thread
            def callback(recognizer, audio):
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
                except sr.UnknownValueError:
                    logging.warn("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))

            # use the microphone as source for input.
            mic = sr.Microphone()
            with mic as source:
                logging.info("Listening To Mic Input")
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                self.r.adjust_for_ambient_noise(source)

            #listens for the user's input 
            return self.r.listen_in_background(mic, callback)
                
        except sr.RequestError as e:
            logging.info("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            logging.info("unknown error occurred")