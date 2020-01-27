#!/bin/bash
docker build . \
    --shm-size 6g \
    -t mousehunt

# create pulseaudio socket
pactl load-module module-native-protocol-unix socket=/tmp/pulseaudio.socket

# create config for pulseaudio clients
echo "default-server = unix:/tmp/pulseaudio.socket
# Prevent a server running in container
autospawn = no
daemon-binary = /bin/true
# Prevent the use of shared memory
enable-shm = false
" >/tmp/pulseaudio.client.conf

# Allow local access to X server
xhost +local:${USER}

docker-compose up -d
