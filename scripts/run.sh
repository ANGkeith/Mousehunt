#!/bin/bash
docker build . \
    --shm-size 6g \
    -t mousehunt

# Allow local access to X server
xhost +local:${USER}

docker-compose up -d
