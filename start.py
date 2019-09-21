# Standard Library
import sys
import logging
from time import sleep

from selenium import webdriver

from MyBot.bot import Bot
from MyBot.utils import noise_generator, get_current_time

# logger
LOG_FILE = f"{sys.argv[1]}.log"
URL = "https://www.mousehuntgame.com"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

driver = webdriver.Firefox()
driver.implicitly_wait(15)
driver.get(URL)


myBot = Bot(driver)
myBot.sign_in(sys.argv[1], sys.argv[2])


while True:
    if myBot.has_king_reward():
        logging.info(
            f"{sys.argv[1]}:{get_current_time()}: "
            f"Time left: {myBot.get_time_left()} | "
            f"Kings Reward! Please collect your reward! | "
            f"Horn Count: {myBot.horncount}"
        )
        sleep(90)
    elif myBot.is_ready():
        sleep(noise_generator())
        myBot.sound_horn()
    else:
        logging.info(
            f"{sys.argv[1]}:{get_current_time()}: "
            f"Time left: {myBot.get_time_left()} | "
            f"Horn Count: {myBot.horncount}"
        )
        sleep(90)
