#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

source ${project_root}/.env

# check if lock file exists, if not, creates it
if [[ ! -e /tmp/mousehunt-notif.lock ]]; then
    touch /tmp/mousehunt-notif.lock;
    dunstify --appname="Mousehunt" --icon="~/.local/share/icons/mousehunt.png" "Mousehunt notification has started"
fi

# Splitting the colon separated variables into arrays
IFS=: read -a usernames  <<< $usernames

response=$(curl http://$ip:$port)

echo $response

kings_reward=$(echo "$response" | grep -B 1 "Kings Reward")
connection_timeout=$(echo "$response" | grep "Connection timed out")

if [[ ! -z $connection_timeout ]]; then
    dunstify --appname="Mousehunt" --icon="~/.local/share/icons/mousehunt.png" "Connection timeout.
(Mostly, wrong ip address)";
fi

num_of_users=${#usernames[@]}

for (( i=0; i<$num_of_users; i++ )); do
    username=${usernames[@]:$i:1}

    if [[ $kings_reward == *"${username}"* ]]; then
        echo "$username"
        dunstify --appname="Mousehunt" --icon="~/.local/share/icons/mousehunt.png" "$username has kings reward";
    fi
done
