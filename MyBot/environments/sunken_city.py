# Standard Library
from typing import Any

from MyBot.bot import Bot
from MyBot.hud import armCharm, disArmCharm

ANCHOR_ZONE = [
    "Sunken Treasure",
    "Pearl Patch",
    "Sand Dollar Sea Bar",
    "Oxygen Stream",
    "Deep Oxygen Stream",
]


def prepare(bot: Bot) -> None:
    anchor_charm = bot.driver.find_elements_by_class_name("charm")[0]

    if is_anchor_zone(bot):
        armCharm(anchor_charm)
    else:
        disArmCharm(anchor_charm)


def is_anchor_zone(bot: Bot) -> bool:
    return (
        bot.driver.find_elements_by_class_name("zoneName")[0].get_attribute(
            "innerText"
        )
        in ANCHOR_ZONE
    )
