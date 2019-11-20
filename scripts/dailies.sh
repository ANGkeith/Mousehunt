#!/bin/bash
docker build . \
    --shm-size 6g \
    -t mousehunt

# Allow local access to X server
xhost +local:${USER}

docker run -it \
        --rm \
        --name mousehunt_bot_dailies \
        --shm-size 6g \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -e DISPLAY=unix${DISPLAY} \
        --env-file .env \
        --user $(id -u):$(id -g) \
        mousehunt \
        ./scripts/dailies.sh
