#!/bin/bash
script_directory=$(cd $(dirname ${BASH_SOURCE}) && pwd -P)
project_root=$(cd $(dirname ${script_directory}) && pwd -P)

cd $project_root
FLASK_APP="${project_root}"/flask_server.py "$HOME"/.local/bin/flask run --host 0.0.0.0 --port 54321
