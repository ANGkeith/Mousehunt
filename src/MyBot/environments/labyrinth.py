# Standard Library

import logging
from time import sleep
from typing import List

# Third Party Library
from selenium.webdriver.remote.webelement import WebElement

# My Libary
from MyBot.bot import Bot
from MyBot.utils import notify
from MyBot.settings import AFK_MODE, PREFERED_HALLWAY_TYPE, env
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

HALLWAY_QUALITIES = ["Plain", "Superior", "Epic"]
HALLWAY_LENGTHS = ["Short", "Medium", "Long"]
HALLWAY_TYPES = ["Fealty", "Tech", "Scholar", "Farming", "Treasury"]

SHUFFLE_LIMIT = 5


def prepare(bot: Bot) -> None:
    if (
        is_at_intersection(bot)
        and env.str(PREFERED_HALLWAY_TYPE) in HALLWAY_TYPES
    ):
        for i in range(SHUFFLE_LIMIT):
            if has_preferred_hallway(bot):
                select_door(bot)
                break
            else:
                shuffle_door(bot)
                sleep(1)

            if i == SHUFFLE_LIMIT - 1:
                afk_mode(bot)

    elif is_at_exit(bot) or is_at_entrance(bot) or is_at_intersection(bot):
        logger.info(("Labyrinth intersection."))
        notify("is at a Labyrinth intersection.")
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


def has_preferred_hallway(bot: Bot) -> bool:
    web_elements = get_current_door_web_elements(bot)
    doors = [web_element.get_attribute("text") for web_element in web_elements]
    logger.info(f"Current Door: {doors}")
    for web_element in web_elements:
        if env.str(PREFERED_HALLWAY_TYPE) in web_element.get_attribute("text"):
            return True
    return False


def get_current_door_web_elements(bot: Bot) -> List:
    return bot.driver.find_elements_by_class_name("labyrinthHUD-doorContainer")[
        0
    ].find_elements_by_class_name("labyrinthHUD-door")


def compute_score(door_name: str) -> int:
    score = 0

    for i, length in enumerate(HALLWAY_LENGTHS):
        if length in door_name:
            score += i + 1

    for i, quality in enumerate(HALLWAY_QUALITIES):
        if quality in door_name:
            score += (i + 1) * 10

    if env.str(PREFERED_HALLWAY_TYPE) in door_name:
        score += 100

    return score


def get_best_door_web_ele(bot: Bot) -> WebElement:
    web_elements = get_current_door_web_elements(bot)
    best_score = 0

    for web_ele in web_elements:
        logger.debug(
            f"{web_ele.get_attribute('text')} has a score of {compute_score(web_ele.get_attribute('text'))}"
        )
        cur_score = compute_score(web_ele.get_attribute("text"))
        if best_score < cur_score:
            best_score = cur_score
            best_door_web_ele = web_ele
    return best_door_web_ele


def shuffle_door(bot: Bot) -> None:
    # click on shuffle doors
    bot.driver.find_element_by_class_name(
        "labyrinthHUD-scrambleDoors-boundingBox"
    ).click()
    # use shuffle cube
    bot.driver.find_element_by_class_name("confirm").click()
    logger.info("Shuffle door")


def select_door(bot: Bot) -> None:
    best_door_web_ele = get_best_door_web_ele(bot)
    # click on best door
    best_door_web_ele.click()
    # confirm
    bot.driver.find_element_by_class_name("confirm").click()
    logger.info(f"Select {best_door_web_ele.get_attribute('text')} door")
