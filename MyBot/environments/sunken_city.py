from MyBot.bot import Bot
from MyBot.hud import disArmCharm, armCharm
from typing import Any

ANCHOR_ZONE = ["Sunken Treasure", "Pearl Patch", "Sand Dollar Sea Bar", "Oxygen Stream", "Deep Oxygen Strem"]


def prepare(bot: Bot) -> None:
    anchor_charm = bot.driver.find_elements_by_class_name("charm")[0]

    if is_anchor_zone(bot):
        armCharm(anchor_charm)
    else:
        disArmCharm(anchor_charm)


def is_anchor_zone(bot: Bot) -> bool:
    return bot.driver.find_elements_by_class_name("zoneName") in ANCHOR_ZONE
