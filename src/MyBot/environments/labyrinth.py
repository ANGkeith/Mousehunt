# Standard Library

from time import sleep

from MyBot.bot import Bot
from MyBot.utils import play_sound
from MyBot.environments.sunken_city import afk_mode


def prepare(bot: Bot) -> None:
    if is_at_exit(bot) or is_at_intersection(bot) or is_at_entrance(bot):
        play_sound()
        sleep(60)
        if is_at_exit(bot) or is_at_intersection(bot) or is_at_entrance(bot):
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
