# Standard Library
import re
from time import sleep

from MyBot.bot import Bot
from MyBot.hud import armCharm, disArmCharm

ANCHOR_ZONE = [
    "Sunken Treasure",
    "Pearl Patch",
    "Sand Dollar Sea Bar",
    "Oxygen Stream",
    "Deep Oxygen Stream",
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
    latest_journal_entry = bot.driver.find_elements_by_xpath(
        "//div[@id='journalContainer']"
        "//div[@class='content']"
        "//div[@data-entry-id]"
    )[0].get_attribute("innerText")
    return "I finished exploring" in latest_journal_entry


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
