#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

mousehunt_build=$(cd ${project_root}; docker build . -t mousehunt)
mousehunt_run=$(cd ${project_root}; docker run --entrypoint launch_browser.sh -it --rm --name gui_$1 --shm-size 6g --net host -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix${DISPLAY} --env-file .env_$1 mousehunt)
