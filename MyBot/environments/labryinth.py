# Standard Library

from MyBot.bot import Bot
from MyBot.utils import play_sound


def prepare(bot: Bot) -> None:
    print("i am in labryinth") 
    if is_at_exit() or is_at_intersection():
        play_sound()

    

def is_at_exit(bot: Bot) -> bool:
    return len(bot.driver.find_elements_by_class_name("labyrinthHUD exit")) != 0


def is_at_intersection(bot: Bot) -> bool:
    return len(bot.driver.find_elements_by_class_name("labyrinthHUD exit")) != 0
