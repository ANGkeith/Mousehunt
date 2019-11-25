# Standard Library
import logging

from environs import Env
from MyBot.bot import Bot
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s: %(levelname)-8s: %(name)s %(funcName)s(): %(message)s",
    datefmt="%H:%M:%S",
)

file_handler = logging.FileHandler("bot.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def prepare(bot: Bot) -> None:
    env = Env()
    env.read_env()

    instruction = env("burroughs_rift_intructions")
    try:
        globals()[instruction](bot)
    except KeyError:
        logger.debug(f"The function {instruction} does not exists.")


# helper for burrough rift
def isMisting(bot: Bot) -> bool:
    bot.driver.implicitly_wait(1)
    try:
        bot.driver.find_element_by_class_name("is_misting")
        bot.driver.implicitly_wait(5)
        return True
    except NoSuchElementException:
        bot.driver.implicitly_wait(5)
        return False


def mistIsGTE19(bot: Bot) -> bool:
    return (
        int(
            bot.driver.find_elements_by_class_name("mistQuantity")[0]
            .get_attribute("innerText")
            .split("/")[0]
        )
        >= 19
    )


def mistIsGTE16(bot: Bot) -> bool:
    return (
        int(
            bot.driver.find_elements_by_class_name("mistQuantity")[0]
            .get_attribute("innerText")
            .split("/")[0]
        )
        >= 16
    )


def toggleMist(bot: Bot) -> None:
    bot.driver.find_elements_by_class_name("mistButton")[0].click()


def onMist(bot: Bot) -> None:
    if isMisting(bot):
        pass
    else:
        toggleMist(bot)


def offMist(bot: Bot) -> None:
    if isMisting(bot):
        toggleMist(bot)
    else:
        pass


def maintainMistInRed(bot: Bot) -> None:
    if mistIsGTE19(bot):
        offMist(bot)
    else:
        onMist(bot)


def maintainMistInGreen(bot: Bot) -> None:
    if mistIsGTE16(bot):
        offMist(bot)
    else:
        onMist(bot)
