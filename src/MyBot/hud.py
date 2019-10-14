# Standard Library
from typing import Any

from MyBot.bot import Bot


def armCharm(bot: Bot, charm_title: str) -> None:
    """
    Used to arm charms from HUD

    :param charm_title: The title attribute of the charm to arm
    """
    charm_element = get_charm_element(bot, charm_title)

    if not isArmed(charm_element):
        charm_element.click()


def disArmCharm(bot: Bot, charm_title: str) -> None:
    """
    Used to disarm charm from HUD

    :param charm_title: The title attribute of the charm to disarm
    """
    charm_element = get_charm_element(bot, charm_title)

    if isArmed(charm_element):
        charm_element.click()


def get_charm_element(bot: Bot, charm_title: str) -> Any:
    """
    Used to recurse through the charm elements to get the element with the title
    attribute = `charm_title`

    :param charm_title: The title attribute of the charm to disarm
    """
    hud_charms = bot.driver.find_elements_by_class_name("charm")
    for c in hud_charms:
        if charm_title == c.get_attribute("title"):
            return c


def isArmed(element: Any) -> bool:
    """
    Used to check whether the charm is armed from HUD

    :param element: driver.find_elements_by_class_name("charm")[i] where i is
    the index of choice
    """
    return element.get_attribute("class") == "charm active"


def go_to_camp_page(bot: Bot) -> None:
    bot.driver.find_element_by_xpath(
        "//li[@class='camp']//a[@class='mousehuntHud-menu-item root']"
    ).click()
