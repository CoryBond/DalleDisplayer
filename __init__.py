
import tkinter as tk
import logging
from datetime import datetime

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

now = datetime.now() # current date and time
timeStr = now.strftime("%H:%M:%S")

logger.info("hello world " + timeStr)

def on_button_click():
    print("Button clicked!")

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Create a button and pack it into the window
button = tk.Button(root, text="Click me!", command=on_button_click)
button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
