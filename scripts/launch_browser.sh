#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

source ${project_root}/.env

# Splitting the colon separated variables into arrays
IFS=: read -a usernames  <<< $usernames

num_of_users=${#usernames[@]}
for (( i=0; i<$num_of_users; i++ )); do
    username=${usernames[@]:$i:1}
    docker exec -d $username gui.sh
done
