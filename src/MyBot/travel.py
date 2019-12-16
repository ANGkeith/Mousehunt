# Standard Library
from time import sleep

# My Libary
from MyBot.bot import Bot


def travel(bot: Bot, region: str, environment: str) -> None:
    """
    :params region: name of the region
    :params environments: name of the environment
    """
    go_to_travel_page(bot)
    sleep(1)
    select_region(bot, region)
    sleep(1)
    select_environment(bot, environment)
    sleep(1)
    travel_to_environment(bot)
    sleep(1)
    bot.go_to_main_page()


def go_to_travel_page(bot: Bot) -> None:
    bot.driver.find_element_by_xpath("//div[contains(text(),'Travel')]").click()


def select_region(bot: Bot, region: str) -> None:
    regions = bot.driver.find_elements_by_xpath(
        "//a[@class='travelPage-map-region-name']"
    )
    for r in regions:
        if region == r.text:
            r.click()


def select_environment(bot: Bot, environment: str) -> None:
    environments = bot.driver.find_elements_by_xpath(
        "//div[@class='travelPage-map-region active']"
        "//a[@class='travelPage-map-region-environment-link ']"
    )
    for e in environments:
        if environment == e.text:
            e.click()


def travel_to_environment(bot: Bot) -> None:
    element = bot.driver.find_element_by_xpath(
        "//div[contains(@class,'travelPage-map-image-wrapper')]"
        "//div[contains(@class,'highlight')]"
        "//div[@class='travelPage-map-image-environment-button']"
    )
    element.click()
