#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

source ${project_root}/.env

# Splitting the colon separated variables into arrays
IFS=: read -a usernames  <<< $usernames

num_of_users=${#usernames[@]}
for (( i=0; i<$num_of_users; i++ )); do
    username=${usernames[@]:$i:1}
    python3 ${project_root}/scripts/find_and_replace.py "delete_raffle_tickets\=False\n" "delete_raffle_tickets=True\n" "${project_root}/.env_$username"
done
