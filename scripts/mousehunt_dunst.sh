#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

source ${project_root}/.env

notify_with_dunst() {
    ACTION=$(dunstify --appname="Mousehunt" --icon="~/.local/share/icons/mousehunt.png" --action="default,Launch Browser" "$1: $2")

    case "$ACTION" in
    "default")
        ${project_root}/scripts/launch_browser.sh $1 &
        # Todo: reload the server
        ;;
    esac
}

# check if lock file exists, if not, creates it
if [[ ! -e /tmp/mousehunt-notif.lock ]]; then
    touch /tmp/mousehunt-notif.lock;
    dunstify --appname="Mousehunt" --icon="~/.local/share/icons/mousehunt.png" "Mousehunt notification has started"
fi

messages=$(curl -s $ip:$port | jq '[.data[] | select(.message!="All Good")]')

number_of_message=$(jq 'length' <<< $messages)

for (( i=0; i<$number_of_message; i++ )); do
    username=$(jq -r ".[$i].username" <<< $messages)
    message=$(jq -r ".[$i].message" <<< $messages)

    notify_with_dunst $username "$message"
done
