#!/usr/bin/python3
# Third Party Library
# Standard Library
import subprocess

from flask import Flask

app = Flask(__name__)

@app.route("/logs")
def logs():
    cmd = "make status"
    return subprocess.getoutput(cmd)

@app.route("/refresh")
def refresh():
    cmd = "make refresh"
    return subprocess.getoutput(cmd)

if __name__ == "__main__":
    app.run(debug=False)
