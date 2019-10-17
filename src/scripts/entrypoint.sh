#!/bin/bash

# Splitting the colon separated variables into arrays
IFS=: read -a passwords <<< $passwords
IFS=: read -a usernames  <<< $usernames

mkdir log
num_of_users=${#usernames[@]}
for (( i=0; i<num_of_users; i++ )); do
    touch ./log/${usernames[@]:$i:1}.log
    python3 start.py ${usernames[@]:$i:1} ${passwords[@]:$i:1} &
done

# Use to prevent the script from exiting
tail -f ./log/*.log
