# Standard Library
import os
import sys
import time
import random
from datetime import datetime


def noise_generator() -> int:
    """
    Used to generate random int
    """
    return 42 + random.randint(1, 30)


def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def to_lower_case_with_underscore(string: str) -> str:
    return string.lower().replace(" ", "_")


def is_sleeping_time() -> bool:
    return int(time.strftime("%H")) < 5


def no_sound_time() -> bool:
    return int(time.strftime("%H")) < 10


def play_sound() -> None:
    duration = 1  # seconds
    freq = 200  # Hz
    os.system("play -nq -t alsa synth {} sine {}&".format(duration, freq))


def log_identifier() -> str:
    return f"{get_current_time()}:"


def color_red(message: str) -> str:
    return "\x1b[5;30;41m" + message + "\x1b[0m"


def color_green(message: str) -> str:
    return "\x1b[1;32;40m" + message + "\x1b[0m"


def get_latest_journal_entry(bot: "Bot") -> str:
    return bot.driver.find_element_by_id("journallatestentry").text
