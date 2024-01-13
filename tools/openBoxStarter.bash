#!/bin/bash

subPath="src"
while getopts "t" arg; do
    case $arg in
        t) 
            echo "Using test UI" 
            subPath="test";;
    esac

done

echo "killing old instance"

kill $(ps aux | grep 'openbox' | awk '{print $2}')

echo starting openbox with python application

DISPLAY=:0.0 openbox --debug --startup "python3 $HOME/python/PAIID/${subPath}/main.py"