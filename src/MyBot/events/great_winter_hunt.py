# Standard Library
import logging

# Third Party Library
# unchingThird Party Library
from selenium.common.exceptions import NoSuchElementException

# My Libary
from MyBot.bot import Bot

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
        logger.info("Golem(s) have returned")
        claim_golems(bot)
    else:
        logger.info("Golem(s) not back yet")

    if golem_ready(bot):
        logger.info("Golem(s) ready")
        launch_golems(bot)


def golem_returned(bot: Bot) -> bool:
    try:
        number_of_golem_returned = len(
            bot.driver.find_element_by_class_name(
                "winterHunt2019HUD-golemContainer"
            ).find_elements_by_xpath(
                "//div[contains(@class, 'winterHunt2019HUD-golemBuilder  mousehuntTooltipParent canClaim plural')]"  # noqa: E501 pylint: disable=C0301
            )
        )
        return number_of_golem_returned > 0
    except NoSuchElementException:
        return False


def claim_golems(bot: Bot) -> None:
    claimable_golems = bot.driver.find_element_by_class_name(
        "winterHunt2019HUD-golemContainer"
    ).find_elements_by_xpath(
        "//div[contains(@class, 'winterHunt2019HUD-golemBuilder  mousehuntTooltipParent canClaim plural')]"  # noqa: E501 pylint: disable=C0301
    )
    logger.info(f"Claiming { len(claimable_golems) } golems")

    for golem in claimable_golems:
        golem.click()
        bot.driver.find_element_by_xpath(
            "//a[contains(@class, 'jsDialogClose')]"
        ).click()
    logger.info("Golem(s) claimed")


def golem_ready(bot: Bot) -> bool:
    try:
        number_of_golem_returned = len(
            bot.driver.find_element_by_class_name(
                "winterHunt2019HUD-golemContainer"
            ).find_elements_by_xpath(
                "//div[contains(@class, 'winterHunt2019HUD-golemBuilder  mousehuntTooltipParent canBuild plural')]"  # noqa: E501 pylint: disable=C0301
            )
        )
        return number_of_golem_returned > 0
    except NoSuchElementException:
        return False


def launch_golems(bot: Bot) -> None:
    launchable_golems = bot.driver.find_element_by_class_name(
        "winterHunt2019HUD-golemContainer"
    ).find_elements_by_xpath(
        "//div[contains(@class, 'winterHunt2019HUD-golemBuilder  mousehuntTooltipParent canBuild plural')]"  # noqa: E501 pylint: disable=C0301
    )
    logger.info(f"Launching { len(launchable_golems) } golems")

    for golem in launchable_golems:
        golem.click()
        bot.driver.find_element_by_xpath(
            "//div[contains(@class, 'winterHunt2019HUD-popup-tabContent build visible')]"  # noqa: E501 pylint: disable=C0301
            "//div[contains(@class, 'winterHunt2019HUD-popup-golem canBuild visible')]"  # noqa: E501 pylint: disable=C0301
            "//div[contains(@class, 'winterHunt2019HUD-popup-golemState canBuild empty canClaim')]"  # noqa: E501 pylint: disable=C0301
            "//a[@class='winterHunt2019HUD-popup-sendGolemButton']"  # noqa: E501 pylint: disable=C0301
        ).click()
    logger.info("Golem(s) launched")
