
from tkinter import *
import logging
from PIL import Image, ImageTk

from imageProviders.ImageProvider import ImageProvider
from utils.utils import get_project_root
from utils.loggingUtils import generate_logger

class RootWindow(object):


    def __init__(self, imageProvider: ImageProvider):

        self.logger = generate_logger(self.__class__.__name__)

        self.imageProvider = imageProvider

        root = Tk()
        root.attributes('-fullscreen', True)
        root.title("DalleDisplayer")
        self.root = root

        label = Label(self.root)
        self.label = label

        return


    def update_image(self, image): 

        display = ImageTk.PhotoImage(image)

        self.label.configure(image=display)
        self.label.image=display
        self.label.pack(side="bottom", fill="both", expand="yes")

    def on_button_click(self):
            image = self.imageProvider.get_image_from_string("A cool turtle with shades")
            image.save(get_project_root()/'..'/'test.png', "PNG");
            self.update_image(image)

    def start(self):

        # Create the main window

        # Create a button and pack it into the window
        button = Button(self.root, text="Click me!", command=self.on_button_click)
        button.pack(pady=10)

        image  = Image.open(get_project_root()/'..'/'test.png')

        self.update_image(image)

        # Run the Tkinter event loop
        self.root.mainloop()

        return