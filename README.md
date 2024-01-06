# 🍱 DalleDisplayer

DalleDisplayer is a program originally designed for a single board computer (a raspberry pi 3 specifically) that displays Dalle Images to a connected screen. It is planned to support voice commands, touch screens and remote commands. These will all be incremental features!

This is a side project I am working on as I upgraded my retropie gaming system to the new raspbery pi 5 and want to do a cool project with my old raspberry pi 3. In particular I am interested in doing something AI related as the latest developments in AI tools (like ChatGPT 4) seem to have lots of pratical utility in peoples lives. Setting aside the controversies arising from AI tools I want to get more involved in developing with them both for my job and for fun.

## 🗺️ Roadmap

1. Run a python GUI on a monitor [✅]
2. Create a git repo for the project [✅]
3. Boot the DalleDisplayer GUI on device start [✅]
4. Connect 7 inch touchscreen display to the pi [✅]
5. Boot GUI to connected touchscreen [✅]
6. Wire the touchscreen to the board [✅]
7. Install the Dalle Python client. [✅]
8. Pay for a client subscription. [✅]
9. Display Dalle Images to screen via hardcoded prompts.
10. Connect usb microphone to the device (might be more difficult then it ... sounds) [✅]
11. Support voice commands when a user touches a "make image" button.

## Running The Program

This project was built in Python3.11 on a Raspberry Pi 3 with a arm7 (32 bit) chipset. Python3.11 is not the default python version of earlier RaspberryPi OS (its 3.7.x) and its not recommended you change the default python version of those systems in case of breaking other scripts on the plateform. Instead its recommended you install 3.8+ seperatly. Its possible to do this by installing the source code and compilling from scratch. See: https://itheo.tech/install-python-38-on-a-raspberry-pi
Its recommended to make the virtual python env using Python3.11 rather then Python3.7 with `Python3.11 -m env myenv`.

If using a virtual env and `Python3.11 dalle.py` doesn't work or is giving you weird dependency errors you can try to the scripts with the python interpreter directly in myenv. Something like `*PATH_TO_DALLE_DISPLAYER*/myenv/bin/python dalle.py`. I have seen this on my machine but don't really know how to fix it so that running Python3.11 from the virtual environment will use the right interpreter.

## 🏴󠁶󠁥󠁷󠁿 Dependencies

Almost all python packages required by this project can be found in the requirements.txt and can be imported into a python environment using:
`python3 -m pip install -r requirements.txt` after starting your pytho env `source myenv/bin/activate`.

### Additional Package Installs

Some packages, like speech_recognition, also require additional system specific packages if they don't already exist. You might have to install
these manually prior to using DalleDisplayer.
For example:

| System | Package | Install Command                      | Required By        |
| ------ | ------- | ------------------------------------ | ------------------ |
| Linx   | tKinter | sudo apt-get install python3-tk      | tKinter            |
| Linx   | PyAudio | sudo apt-get install python3-pyaudio | pyaudio            |
| Linx   | Flac    | sudo apt-get install flac            | speech_recognition |
| Linx   | ESpeak  | sudo apt-get install espeak          | speech_recognition |

### PiWheels

Newer versions of packages, specifically numpy, can take absurd amounts of time to compile and download on a rasbperry pi. To avoid this only use the numpy version specified in the requirements file and setup pre-compiled pi [wheels](https://www.piwheels.org/) installations in the `etc/pip.config`.

## 📶 How to display GUI through SSH / Remote VSCode

If on a windows machine and you want to display this GUI back through SSH to the client then do the following:

1. Install and run https://sourceforge.net/projects/xming/
2. Make sure the SSH session uses ForwardX11 :
3. The following configs in VSCode can be set : -ForwardAgent yes -ForwardX11 yes -ForwardX11Trusted yes

And this should make it work!

## 🖥️ How to display GUI on connected monitor

Dalle Displayer can run in either Desktop Environments or in Window Manger environments though the later will require some extra work to setup.

### No Desktop Environment

Before you can display this program onto a connected monitor you must first setup a display server and window manager for the GUI. Assuming you work in a headless environment you can use xinit + openbox for this as follows:

1. Install xinit openbox
   (NOTE: [xinit](https://en.wikipedia.org/wiki/Xinit) is display server while [openbox]() is a graphical window manager. Together these will allow rendering the python GUI to a connected monitor. )
2. Create a directory/file called at `~/.config/openbox/autostart`
   1. Add an entry in that file as `python3 ~path_to_DalleDisplayer_root~/src/main.py` (autostart runs everytime the openbox-session [not the openbox command line] runs)

After following these steps you can now run `xinit openbox-session` and it will should start up the DalleDisplayer and render the GUI to the connected monitor.
If the DalleDisplayer closes while openbox-session is still up you can do a few things to restart it:

1. Restart xinit + openbox
2. Run the script directly while openbox session is open with `DISPLAY=:0.0 python3 ~path_to_DalleDisplayer_root~/src/main.py`

#### Boot

Several linux tools allow xinit + openbox + DalleDisplayer to start at boot though I recommend using crontab. Using rc.local to load startx did not cause openbox to detect the user specific `~/.config/openbox/autostart`` script.

After opening `crontab -e` all you need to do is add a line like `@reboot xinit openbox-session`. If you also setup DalleDisplayer in the openbox autostart file then it will load at boot as well.

#### OpenBox command line

I have tried making a start script to run openbox and launch the DalleDisplayer program directly without the need of configuring a external autostrat script but have been unsuccessful. Openbox seems to not run the program at all
and hangs. To run this script you can execute the command `startx ./openBoxStarter.bash` though it might not work.

This script was made via a suggestion in https://raspberrypi.stackexchange.com/questions/98944/launch-a-gui-tkinter-program-on-boot.

#### Calibrating Touchscreen

For touchscreens its possible for the input to off.... sometimes very off. In a headless environment there is a tool
that uses xinit to recalibrate the input. Simply install [xinput_calibrator](xinput_calibrator) and run it with `startx`
