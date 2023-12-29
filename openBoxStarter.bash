#!/bin/bash

echo $SHLVL

# If this script is not run with the "script" application then wrap it into a script application to log all output to a log file.
#if [[ $SHLVL -eq 3 ]] ; 
#then 
#    /usr/bin/script log.txt /bin/bash -c "$0 $*"
#    exit 0
#fi

echo starting openbox with python application

openbox --debug --config-file ~/.config/openbox/rc.xml --startup ./__init__.py
