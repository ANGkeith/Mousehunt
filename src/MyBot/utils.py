# Standard Library
import os
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
    return int(time.strftime("%H")) < 7


def play_sound() -> None:
    duration = 5  # seconds
    freq = 200  # Hz
    # For Linux only, sudo apt install sox
    os.system("play -nq -t alsa synth {} sine {}&".format(duration, freq))