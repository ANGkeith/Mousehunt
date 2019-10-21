#!/bin/bash

# Splitting the colon separated variables into arrays
IFS=: read -a passwords <<< $passwords
IFS=: read -a usernames  <<< $usernames

mkdir log
num_of_users=${#usernames[@]}
touch MyBot.log
for (( i=0; i<num_of_users; i++ )); do
    python3 start.py ${usernames[@]:$i:1} ${passwords[@]:$i:1} &
done

# sound_check
play -nq -t alsa synth 1 sine 200

# Use to prevent the script from exiting
tail -f ./MyBot.log
