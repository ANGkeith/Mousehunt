#!/bin/bash

if [ ! -d ./log ]; then
    mkdir log
fi

# sound_check
espeak 'Launching bot' --stdout | paplay

python3 start.py&


# Use to prevent the script from exiting
tail -f /dev/null
