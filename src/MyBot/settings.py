# Standard Library
import sys

# Third Party Library
from environs import Env

env = Env()
env.read_env()

# Settings
NORMAL_DELAY = 60
NIGHT_TIME_DELAY = 3000
URL = "https://www.mousehuntgame.com"
PATH_TO_ENV_FILE = "/app/.env"
REFRESH_QUOTA = 7


# .env Settings
ENV_DAILIES = "dailies"
DELETE_RAFFLE_TICKETS = "delete_raffle_tickets"
COLLECT_DAILIES = "collect_dailies"
AFK_MODE = "afk_mode"
REFRESH = "refresh"
