# Standard Library
import sys
import random
import logging
from time import sleep

from selenium import webdriver

from MyBot.bot import Bot
from MyBot.utils import noise_generator, get_current_time, is_sleeping_time

# Settings
NORMAL_DELAY = 75
NIGHT_TIME_DELAY = 3000

# logger
LOG_FILE = f"{sys.argv[1]}.log"
URL = "https://www.mousehuntgame.com"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

driver = webdriver.Firefox()
driver.implicitly_wait(15)
driver.get(URL)

myBot = Bot(driver)
myBot.sign_in(sys.argv[1], sys.argv[2])


def start() -> None:
    if myBot.has_king_reward():
        logging.info(
            f"{sys.argv[1]}:{get_current_time()}: "
            f"Time left: {myBot.get_time_left()} | "
            f"Kings Reward! Please collect your reward! | "
            f"Horn Count: {myBot.horncount}"
        )
        sleep(NORMAL_DELAY)
    elif myBot.is_ready():
        # wait for random amount of time before sounding horn again
        sleep(noise_generator())
        myBot.sound_horn()
        print(f"{sys.argv[1]} sounded {myBot.horncount} times")
    else:
        myBot.prepare()
        logging.info(
            f"{sys.argv[1]}:{get_current_time()}: "
            f"Time left: {myBot.get_time_left()} | "
            f"Horn Count: {myBot.horncount}"
        )
        if is_sleeping_time():
            sleep(NIGHT_TIME_DELAY + random.randint(600, 1200))
        else:
            sleep(NORMAL_DELAY)


while True:
    try:
        start()
    except Exception as e:
        logging.error(e)
        pass
