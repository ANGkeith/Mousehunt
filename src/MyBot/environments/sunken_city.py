# Standard Library
import re
import logging
from time import sleep

from MyBot.bot import Bot
from MyBot.hud import armCharm, disArmCharm
from MyBot.utils import get_latest_journal_entry
from MyBot.travel import travel

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

ANCHOR_ZONE = [
    "Sunken Treasure",
    "Pearl Patch",
    "Sand Dollar Sea Bar",
    "Oxygen Stream",
    "Deep Oxygen Stream",
    "Lair of the Ancients",
]

JET_ZONE = ["Shallow Shoals", "Sea Floor", "Murky Depths"]


def prepare(bot: Bot) -> None:
    if is_anchor_zone(bot):
        armCharm(bot, "Anchor Charm")
    else:
        disArmCharm(bot, "Anchor Charm")

        if just_finish_exploring(bot) and needs_jet(bot):
            armCharm(bot, "Water Jet Charm")


def is_anchor_zone(bot: Bot) -> bool:
    return (
        bot.driver.find_elements_by_class_name("zoneName")[0].get_attribute(
            "innerText"
        )
        in ANCHOR_ZONE
    )


def just_finish_exploring(bot: Bot) -> bool:
    """
    Look at the latest_journal_entry to see if it has finished_exploring
    """
    return "I finished exploring" in get_latest_journal_entry(bot)


def needs_jet(bot: Bot) -> bool:
    bot.driver.find_element_by_class_name("player").click()
    sleep(2)
    should_jet = get_current_zone_length(bot) >= 500
    bot.driver.refresh()
    if should_jet:
        return (
            bot.driver.find_element_by_class_name("zoneName").text in JET_ZONE
        )
    return False


def get_current_zone_length(bot: Bot) -> int:
    """
    Used for getting the current zone length as shown in the sonar periscope. It
    returns 0 if not found
    """
    result = re.search(
        "[0-9]+",
        bot.driver.find_element_by_xpath(
            "//div[@class='content']"
            "//div[@class='water']"
            "//div[contains(@class, 'active')]"
            "//div[@class='length']"
        ).text,
    )
    if result:
        return int(result.group())
    else:
        return 0


def afk_mode(bot: Bot) -> None:
    logger.debug("Travelling to Sunken City")
    travel(bot, "Rodentia", "Sunken City")
    sleep(0.25)

    logger.debug("Equiping favourite trap 1")
    # equip favourite trap
    bot.driver.find_element_by_xpath(
        "//a[@class='mousehuntHud-userStat trap weapon']"
    ).click()
    sleep(0.25)
    bot.driver.find_element_by_xpath(
        "//div[@class='campPage-trap-itemBrowser-favorite-item  '][1]"
    ).click()
    sleep(0.25)

    logger.debug("Equiping favourite base 1")
    bot.driver.find_element_by_xpath(
        "//a[@class='mousehuntHud-userStat trap base']"
    ).click()
    sleep(0.25)
    bot.driver.find_element_by_xpath(
        "//div[@class='campPage-trap-itemBrowser-favorite-item  '][1]"
    ).click()
    sleep(0.25)

    bot.go_to_main_page()
