# Standard Library

import logging
from time import sleep

# My Libary
from MyBot.bot import Bot
from MyBot.utils import notify
from MyBot.settings import AFK_MODE, env
from MyBot.environments.sunken_city import afk_mode

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
    if is_at_exit(bot) or is_at_intersection(bot) or is_at_entrance(bot):

        logger.info(("Labyrinth intersection."))
        notify("is at a Labyrinth intersection.")
        sleep(60)
        if is_at_exit(bot) or is_at_intersection(bot) or is_at_entrance(bot):
            # if env.bool(AFK_MODE, False):
            afk_mode(bot)


def is_at_exit(bot: Bot) -> bool:
    return (
        bot.driver.find_elements_by_class_name("labyrinthHUD")[0].get_attribute(
            "class"
        )
        == "labyrinthHUD exit"
    )


def is_at_intersection(bot: Bot) -> bool:
    return (
        bot.driver.find_elements_by_class_name("labyrinthHUD")[0].get_attribute(
            "class"
        )
        == "labyrinthHUD intersection"
    )


def is_at_entrance(bot: Bot) -> bool:
    return (
        bot.driver.find_elements_by_class_name("labyrinthHUD")[0].get_attribute(
            "class"
        )
        == "labyrinthHUD intersection entrance"
    )
