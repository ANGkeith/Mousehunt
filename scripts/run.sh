#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

do_this=$(cd ${project_root}; docker-compose up -d --build)

# Allow local access to X server
# xhost +local:${USER}
