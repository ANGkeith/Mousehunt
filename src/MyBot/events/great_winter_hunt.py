# Standard Library
import re
import logging
from time import sleep

from MyBot.bot import Bot
from MyBot.hud import armCharm, disArmCharm
from MyBot.utils import play_sound
from MyBot.travel import travel
from selenium.common.exceptions import NoSuchElementException

# Logger configurations
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


def event(bot: Bot) -> None:
    if golem_returned(bot):
        play_sound()


def golem_returned(bot: Bot) -> bool:
    try:
        number_of_golem_returned = len(
            bot.driver.find_element_by_class_name(
                "winterHunt2019HUD-golemContainer"
            ).find_elements_by_xpath(
                "//div[contains(@class, 'winterHunt2019HUD-golemBuilder  mousehuntTooltipParent canClaim plural')]"
            )
        )
        return number_of_golem_returned > 0
    except NoSuchElementException:
        return False
