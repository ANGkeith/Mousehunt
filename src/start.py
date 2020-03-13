# Standard Library
import random
import logging
from time import sleep

# Third Party Library
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchWindowException,
    InvalidSessionIdException,
)

# My Libary
from MyBot.bot import Bot
from MyBot.utils import notify, color_red

# Logger configurations
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s: %(levelname)-8s: %(name)s %(funcName)s(): %(message)s",
    datefmt="%H:%M:%S",
)

file_handler = logging.FileHandler("bot.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def main() -> None:
    try:
        logger.info(color_red("Starting bot"))
        myBot = Bot()
    except WebDriverException:
        noise = random.randint(43, 73)
        logger.error(
            color_red(
                f"Browser has crashed, going to "
                f"relaunch the browser for one more time in {noise} seconds"
            )
        )
        sleep(noise)
        myBot = Bot()

    number_of_retries = 0

    while True:
        try:
            myBot.start()
        except WebDriverException as e:
            if number_of_retries < 3:
                logger.warning(
                    "Browser has crashed during initial startup, attempting to "
                    "relaunch the browser. (Retries left: "
                    "%d)",
                    3 - number_of_retries,
                )
                logger.exception(e)
                try:
                    myBot.driver.close()
                except InvalidSessionIdException:
                    logger.info("inception")
                except NoSuchWindowException:
                    logger.info("inception")
                number_of_retries += 1
                logger.exception(e)
                myBot = Bot()
                logger.info("Going to sleep for 120 seconds")
                sleep(120)
            else:
                logger.error(color_red(f"Browser has crashed too many times"))
                break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
        notify("has crashed")
