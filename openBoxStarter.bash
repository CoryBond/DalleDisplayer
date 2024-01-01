#!/bin/bash

echo starting openbox with python application

DISPLAY=:0.0 openbox --debug --startup "python3 $HOME/python/DalleDisplayer/src/main.py"