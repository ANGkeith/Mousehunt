#!/bin/bash

if [ ! -d ./log ]; then
    mkdir log
fi

# sound_check
play -nq -t alsa synth 1 sine 200

python3 start.py&


# Use to prevent the script from exiting
tail -f /dev/null
