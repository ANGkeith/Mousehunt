#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

while true; do { echo -e 'HTTP/1.1 200 OK\r\n'; . "${project_root}/scripts/find_and_replace.sh" "refresh"; } | nc -l -N -p 54322; done
