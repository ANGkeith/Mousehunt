import sys
import logging

# Settings
NORMAL_DELAY = 75
NIGHT_TIME_DELAY = 3000
URL = "https://www.mousehuntgame.com"
LOG_DIR = "/var/log/"
LOG_FILE = f"{sys.argv[1]}.log"
URL = "https://www.mousehuntgame.com"
logging.basicConfig(filename=LOG_DIR + LOG_FILE, level=logging.INFO)

