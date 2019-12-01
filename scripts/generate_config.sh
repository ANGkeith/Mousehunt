#!/bin/bash

source ./../.env

cp ../docker-compose.yml.sample ../docker-compose.yml

# Splitting the colon separated variables into arrays
IFS=: read -a passwords <<< $passwords
IFS=: read -a usernames  <<< $usernames


# docker-compose.yml
echo "# Auto-generated with \`generate_docker-compose.sh\`" >> ../docker-compose.yml
num_of_users=${#usernames[@]}
for (( i=0; i<$num_of_users; i++ )); do
    username=${usernames[@]:$i:1}
    password=${passwords[@]:$i:1}

    echo "  $username:
    container_name: $username
    <<: *base
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
      - /tmp/pulseaudio.socket:/tmp/pulseaudio.socket
      - /tmp/pulseaudio.client.conf:/etc/pulse/client.conf
      - .env_$username:/app/.env
    env_file:
      - .env_$username
" >> ../docker-compose.yml

    # .env
    echo "username=$username
password=$password

# burroughs rift
burroughs_rift_instructions=\"maintainMistInGreen\"" > ../.env_$username

    echo "Generated .env_$username successfully"
done

echo "Generated docker-compose.yml successfully"

