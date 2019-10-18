# Standard Library
import sys
import logging
from time import sleep

from MyBot.bot import Bot
from MyBot.utils import log_identifier, noise_generator
from selenium.common.exceptions import WebDriverException


def main() -> None:
    LOG_FILE_PATH = f"log/{sys.argv[1]}.log"
    logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)

    try:
        myBot = Bot()
    except WebDriverException:
        noise = noise_generator()
        logging.error(
            f"{log_identifier()} Browser has crashed, going to "
            f"relaunch the browser for one more time in {noise} seconds"
        )
        sleep(noise)
        myBot = Bot()

    number_of_retries = 0

    while True:
        try:
            myBot.start()
        except WebDriverException:
            if number_of_retries < 3:
                number_of_retries += 1
                logging.error(
                    f"{log_identifier()} Browser has crashed, attempting to "
                    f"relaunch the browser. (Retries left: "
                    "{3 - number_of_retries})"
                )
                myBot = Bot()
            else:
                logging.error(
                    f"{log_identifier()} Browser has crashed too many times. "
                    "Goodbye"
                )
                break
        except Exception as e:
            logging.exception(e)
            break


if __name__ == "__main__":
    main()
