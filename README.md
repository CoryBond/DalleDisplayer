# DalleDisplayer

test

DalleDisplayer is a program originally designed for a single board computer (a raspberry pi 3 specifically) that displays Dalle Images to a connected screen. It is planned to support voice commands, touch screens and remote commands. These will all be incremental features!

This is a side project I am working on as I upgraded my retropie gaming system to the new raspbery pi 5 and want to do a cool project with my old raspberry pi 3. In particular I am interested in doing something AI related as the latest developments in AI tools (like ChatGPT 4) seem to have lots of pratical utility in peoples lives. Setting aside the controversies arising from AI tools I want to get more involved in developing with them both for my job and for fun. 

## Roadmap

1. Run a python GUI on a monitor [SUCCESS]
2. Create a git repo for the project [SUCCESS]
3. Boot the DalleDisplayer GUI on device start.
4. Connect 7 inch touchscreen display to the pi.
  1. Boot GUI to connected touchscreen.
  2. Wire the touchscreen to the board.
5. Install the Dalle Python client.
  1. Pay for a client subscription.
6. Display Dalle Images to screen via hardcoded prompts.
7. Connect usb microphone to the device (might be more difficult then it ... sounds)
8. Support voice commands when a user touches a "make image" button.

7 forward might be more complicated then initially though as the Raspbery Pi 3 apparently does not support input audio and I see meantion of sound boards required to make input audio to work... but I also articles like this : https://raspberrytips.com/add-microphone-raspberry-pi/ which apparently say a usb microphone just works... and with no need for drivers either. When it gets to around 7 it will all be fairly experimental. I will be getting a 7 inch touchscreen display and microphone at the same time so I might do a mini POC for 7 before other steps just to see potential issues.

## How to display GUI through SSH / Remote VSCode

If on a windows machine and you want to display this GUI back through SSH to the client then do the following:
1. Install and run https://sourceforge.net/projects/xming/
2. Make sure the SSH session uses ForwardX11  :
  1. The following configs in VSCode can be set :  -ForwardAgent yes -ForwardX11 yes -ForwardX11Trusted yes

And this should make it work!

## How to display GUI on connected monitor

Dalle Displayer can run in either Desktop Environments or in Window Manger environments though the later will require some extra work to setup.

### No Desktop Environment

Before you can display this program onto a connected monitor you must first setup a display server and window manager for the GUI. Assuming you work in a headless environment you can use xinit + openbox for this as follows:

1. Install xinit openbox
   (NOTE: [xinit](https://en.wikipedia.org/wiki/Xinit) is display server while [openbox]() is a graphical window manager. Together these will allow rendering the python GUI to a connected monitor. )
2. Create a directory/file called at `~/.config/openbox/autostart`
	1. Add an entry in that file as `python3 ~path_to_DalleDisplayer_root~/__init__.py` (autostart runs everytime the openbox-session [not the openbox command line] runs)

After following these steps you can now run `sudo xinit openbox-session` and it will both start up the DalleDisplayer and render the GUI to the connected monitor.
If the DalleDisplayer closes while openbox-session is still up you can do a few things to restart it:

1. Restart xinit + openbox
2. Run the script directly while openbox session is open with `DISPLAY=:0.0 python3 ~path_to_DalleDisplayer_root~/__init__.py`

#### OpenBox command line

I have tried making a start script to run openbox and launch the DalleDisplayer program directly without the need of configuring a external autostrat script but have been unsuccessful. Openbox seems to not run the program at all
and hangs. To run this script you can execute the command `sudo xinit ./openBoxStarter.bash` though it might not work.

This script was made via a suggestion in https://raspberrypi.stackexchange.com/questions/98944/launch-a-gui-tkinter-program-on-boot.
