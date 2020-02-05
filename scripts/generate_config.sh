#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

source ${project_root}/.env

cp ${project_root}/docker-compose.yml.sample ${project_root}/docker-compose.yml

# Splitting the colon separated variables into arrays
IFS=: read -a passwords <<< $passwords
IFS=: read -a usernames  <<< $usernames


# docker-compose.yml
echo "# Auto-generated with \`generate_docker-compose.sh\`" >> ${project_root}/docker-compose.yml
num_of_users=${#usernames[@]}
for (( i=0; i<$num_of_users; i++ )); do
    username=${usernames[@]:$i:1}
    password=${passwords[@]:$i:1}

    echo "  $username:
    container_name: $username
    <<: *base
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
      - .env_$username:/app/.env
      - /home/${USER}/.config/telegram-send.conf:/home/bot/.config/telegram-send.conf
    env_file:
      - .env_$username
" >> ${project_root}/docker-compose.yml

    # .env
    echo "username=$username
password=$password
dailies=False
delete_raffle_tickets=False
collect_dailies=False
afk_mode=False
refresh=False

# burroughs rift
preferred_hallway_type=\"Fealty\"

# burroughs rift
burroughs_rift_instructions=\"maintainMistInGreen\"" > ${project_root}/.env_$username

    echo "Generated .env_$username successfully"
done

echo "Generated docker-compose.yml successfully"


if [[ ! -s ~/.config/telegram-send.conf ]]; then
    echo
    echo "Error: Missing telegram-send configuration file" >&2
    exit 1;
fi
