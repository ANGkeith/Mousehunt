#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

source ${project_root}/.env

# Splitting the colon separated variables into arrays
IFS=: read -a usernames  <<< $usernames

num_of_users=${#usernames[@]}


t="    "
### crafting a json response
echo {
echo "$t\"data\": ["

for (( i=0; i<$num_of_users; i++ )); do
    username=${usernames[@]:$i:1}
    current_log=$(docker logs --tail 1 $username 2>&1 | sed -n -e 's/.*notify_with_dunst: \(.*\)/\1/p')
    echo "$t$t{"
        echo "$t$t$t\"username\": \"${username}\","
        if [[ -z $current_log ]]; then
            current_log="All Good";
        fi
        echo "$t$t$t\"message\": \"${current_log}\"";

    if [[ $i -eq $(( $num_of_users - 1 )) ]]; then
        echo "$t$t}";
    else
        echo "$t$t},";
    fi
done

echo "$t]"
echo }
