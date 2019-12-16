# Standard Library
import os
import sys
import time
from datetime import datetime

# My Libary
from MyBot.settings import PATH_TO_ENV_FILE, env


def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def to_lower_case_with_underscore(string: str) -> str:
    return string.lower().replace(" ", "_")


def is_sleeping_time() -> bool:
    return int(time.strftime("%H")) < 5


def no_sound_time() -> bool:
    return int(time.strftime("%H")) < 10


def espeak(speech: str) -> None:
    username = env("username")
    os.system(f"espeak '{username}, {speech}' --stdout | paplay")

def color_red(message: str) -> str:
    return "\x1b[1;31;40m" + message + "\x1b[0m"


def color_green(message: str) -> str:
    return "\x1b[1;32;40m" + message + "\x1b[0m"


def color_grey(message: str) -> str:
    return "\x1b[1;37;40m" + message + "\x1b[0m"


def get_latest_journal_entry(bot: "Bot") -> str:
    return bot.driver.find_element_by_id("journallatestentry").text


def set_env(field: str, old_value: str, new_value: str) -> None:
    """
    Override the old env with the new value in the .env file
    """
    with open(PATH_TO_ENV_FILE, "r") as file:
        lines = file.readlines()
    with open(PATH_TO_ENV_FILE, "w") as file:
        for i, line in enumerate(lines):
            if line == f"{field}={old_value}\n":
                lines[i] = f"{field}={new_value}\n"
        file.write("".join(lines))
