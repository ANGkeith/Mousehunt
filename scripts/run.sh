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

docker run -it \
        --rm \
        --name mousehunt_bot \
        --shm-size 6g \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=unix${DISPLAY} \
        --env-file .env \
        --env PULSE_SERVER=unix:/tmp/pulseaudio.socket \
        --env PULSE_COOKIE=/tmp/pulseaudio.cookie \
        --volume /tmp/pulseaudio.socket:/tmp/pulseaudio.socket \
        --volume /tmp/pulseaudio.client.conf:/etc/pulse/client.conf \
        --user $(id -u):$(id -g) \
        mousehunt
