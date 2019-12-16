# Standard Library
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
from MyBot.utils import espeak, color_red, log_identifier, noise_generator

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
        noise = noise_generator()
        logger.error(
            color_red(
                f"{log_identifier()} Browser has crashed, going to "
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
                    f"{log_identifier()} Browser has crashed, attempting to "
                    f"relaunch the browser. (Retries left: "
                    f"{3 - number_of_retries})"
                )
                logger.info("Forcing browser to close")
                try:
                    myBot.driver.close()
                except InvalidSessionIdException:
                    logger.info("inception")
                    pass
                except NoSuchWindowException:
                    logger.info("inception")
                    pass
                number_of_retries += 1
                logger.exception(e)
                myBot = Bot()
            else:
                logger.error(
                    color_red(
                        f"{log_identifier()} Browser has crashed too many times"
                    )
                )
                break
        except Exception as e:
            espeak("the bot has crashed. Good bye")
            logger.exception(color_red(str(e)))
            break


if __name__ == "__main__":
    main()
