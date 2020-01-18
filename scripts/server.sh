#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

while true; do { echo -e 'HTTP/1.1 200 OK\r\n'; sh "${project_root}/scripts/status.sh"; } | sudo nc -l -c -p 54321; done
