
import tkinter as tk
import logging
from datetime import datetime

class RootWindow(object):


    def __init__(self):

        # create logger with 'spam_application'
        logger = logging.getLogger('spam_application')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('spam.log')
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        self.logger = logger

        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.title("DalleDisplayer")
        self.root = root

        return


    def start(self):

        def on_button_click():
            print("Button clicked!")

        # Create the main window

        # Create a button and pack it into the window
        button = tk.Button(self.root, text="Click me!", command=on_button_click)
        button.pack(pady=10)

        # Run the Tkinter event loop
        self.root.mainloop()

        return