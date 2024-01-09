
# Python program to translate
# speech to text and text to speech
 
import speech_recognition as sr
import logging

from speechRecognition.SpeechRegonizer import SpeechRecognizer


class GoogleSpeechRecognizer(SpeechRecognizer):


    def __init__(self):
        super().__init__()
        # Initialize the recognizer 
        self.r = sr.Recognizer() 
        return


    def transcribe(self) -> str:
        try:
            
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                logging.info("Listening To Mic Input")
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                self.r.adjust_for_ambient_noise(source2, duration=0.2)
                
                #listens for the user's input 
                audio2 = self.r.listen(source2)
                
                # Using google to recognize audio
                transcription = self.r.recognize_google(audio2)
    
                return transcription
                
        except sr.RequestError as e:
            logging.info("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            logging.info("unknown error occurred")