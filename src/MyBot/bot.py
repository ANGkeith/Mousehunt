# Standard Library
import sys
import random
import logging
import importlib
from time import sleep
from typing import Union
from datetime import datetime

# Third Party Library
from selenium import webdriver
from dataclasses import field, dataclass
from selenium.webdriver import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
)
from selenium.webdriver.firefox.options import Options

# My Libary
from MyBot.utils import (
    set_env,
    color_red,
    color_grey,
    color_green,
    is_sleeping_time,
    jsonify_this_message,
    get_latest_journal_entry,
    to_lower_case_with_underscore,
)
from MyBot.settings import (
    URL,
    REFRESH,
    AFK_MODE,
    ENV_DAILIES,
    NORMAL_DELAY,
    REFRESH_QUOTA,
    COLLECT_DAILIES,
    NIGHT_TIME_DELAY,
    DELETE_RAFFLE_TICKETS,
    env,
)

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


def sign_in(driver: webdriver) -> None:
    username = env("username")
    password = env("password")

    driver.get(URL)
    sleep(1.5)

    # go to log in by mousehunt account
    driver.find_elements_by_class_name("signInText")[0].click()

    # Enter credentials
    user_field = driver.find_elements_by_class_name("username")[3]
    user_field.send_keys(username)
    password_field = driver.find_elements_by_class_name("password")[3]
    sleep(1.5)
    password_field.send_keys(password)

    # Click Login
    driver.find_elements_by_class_name("actionButton")[1].click()
    sleep(1.5)


@dataclass
class Bot:
    driver: webdriver = field(init=False)
    horncount: int = 0
    num_refresh: int = 0

    def __post_init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        # run in the background
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(5)
        sign_in(self.driver)
        logger.info("Signed in, %s", env("username"))

    def start(self) -> None:
        env.read_env(override=True)
        if env.bool(REFRESH, False):
            self.go_to_main_page()
            logger.info("Browser forced to refresh")
            set_env(REFRESH, "True", "False")
        if env.bool(ENV_DAILIES, False):
            self.send_ticket_back()
            self.send_free_gift()
            self.send_ticket_to_recently_active()
            self.send_gift_to_recently_active()
            self.go_to_main_page()
            set_env(ENV_DAILIES, "True", "False")
        if env.bool(COLLECT_DAILIES, False):
            self.collect_dailies()
            set_env(COLLECT_DAILIES, "True", "False")
        if env.bool(DELETE_RAFFLE_TICKETS, False):
            self.delete_daily_ticket()
            set_env(DELETE_RAFFLE_TICKETS, "True", "False")
        if self.has_king_reward():
            if env.bool(AFK_MODE, False):
                self.recover_from_kings_reward()
            else:
                logger.info(jsonify_this_message("Kings Reward"))
                while not env.bool(REFRESH, False):
                    sleep(NORMAL_DELAY)
                    env.read_env(override=True)
        if self.is_ready():
            # wait for random amount of time before sounding horn again
            if is_sleeping_time():
                logger.debug(
                    color_grey(
                        f"Sounding horn less aggressively, {NIGHT_TIME_DELAY}"
                    )
                )
                sleep(NIGHT_TIME_DELAY)
            else:
                noise = random.randint(43, 73)
                logger.debug(
                    color_grey(
                        f"Horn is ready, Sounding horn in {noise} seconds"
                    )
                )
                sleep(noise)
            self.sound_horn()
        self.prepare()
        self.event()
        if self.get_time_left() == "Out of bait!":
            logger.info(jsonify_this_message("Out of Bait"))
        else:
            logger.debug(
                color_grey(
                    f"Horn is not ready yet, still has "
                    f"{self.get_time_left()} to go. (Number of horn "
                    f"sounded so far: {self.horncount})"
                )
            )
        sleep(NORMAL_DELAY)

    def sound_horn(self) -> None:
        hunters_horn = self.driver.find_elements_by_class_name(
            "mousehuntHud-huntersHorn"
        )[0]
        try:
            hunters_horn.click()
            self.go_to_main_page()
            sleep(2)
            self.horncount += 1
            sleep(2)
            logger.info(
                color_green(f"Horn is sounded, taking a break for 12 minutes")
            )
            sleep(1)
            if "Treasure Map Clue" in str(get_latest_journal_entry(self)):
                logger.info(color_green("Found Treasure Map Clue"))
            for _ in range(12):
                sleep(NORMAL_DELAY)
                if int(datetime.now().strftime("%M")) == 45:
                    logger.debug(f"refreshing")
                    self.go_to_main_page()
                    sleep(2)
                    if "Treasure Map Clue" in str(
                        get_latest_journal_entry(self)
                    ):
                        logger.info(color_green("Found Treasure Map Clue"))
                    break
        except ElementClickInterceptedException:
            self.refresh()
        except ElementNotInteractableException:
            self.refresh()
        except Exception as e:
            logger.exception(e)
            sys.exit(1)

    def refresh(self) -> None:
        if self.num_refresh <= REFRESH_QUOTA:
            self.go_to_main_page()
            self.num_refresh += 1
            logger.warning(
                color_red(
                    f"Horn image is intercepted, refreshing "
                    f"page {REFRESH_QUOTA - self.num_refresh}"
                )
            )
        else:
            logger.error(color_red(f"Refreshed too many times, good bye"))
            sys.exit(1)

    def has_king_reward(self) -> bool:
        try:
            horn_container = self.driver.find_element_by_class_name("warning")
        except NoSuchElementException:
            horn_container = None
        try:
            puzzle = self.driver.find_element_by_class_name(
                "mousehuntPage-puzzle"
            )
        except NoSuchElementException:
            puzzle = None
        if (horn_container and horn_container.text) or (puzzle and puzzle.text):
            return True
        return False

    def get_time_left(self) -> str:
        return self.driver.find_element_by_id("huntTimer").get_attribute(
            "innerText"
        )

    def is_ready(self) -> bool:
        return self.get_time_left() == "Ready!"

    def get_location(self) -> str:
        return self.driver.find_elements_by_class_name(
            "mousehuntHud-environmentName"
        )[0].text

    def prepare(self) -> None:
        """
        Executes the prepare() function based on where the user's current
        location
        """
        location = to_lower_case_with_underscore(self.get_location())
        try:
            module = importlib.import_module(f"MyBot.environments.{location}")
            prepare = getattr(module, "prepare")
            prepare(self)
        except ModuleNotFoundError:
            pass

    def event(self) -> None:
        """
        Executes the event() function based on what the current event is.
        """
        try:
            module = importlib.import_module(
                f"MyBot.events.{env('event', None)}"
            )
            event = getattr(module, "event")
            event(self)
        except ModuleNotFoundError:
            pass

    def go_to_main_page(self) -> None:
        self.driver.get(URL)
        sleep(2)

    def delete_daily_ticket(self) -> None:
        """
        Delete ticket from notification
        """
        self.driver.find_element_by_id("hgbar_messages").click()
        notifications = self.driver.find_elements_by_xpath(
            "//div[@class='tab active']"
            "//div[@class='message daily_draw notification ballot']"
        )
        for n in notifications:
            action_chains = ActionChains(self.driver)
            sleep(1)
            action_chains.move_to_element(n).context_click().perform()
            sleep(1)
            n.find_element_by_class_name("delete").click()
            sleep(1)
        logger.info(color_green("Finished cleaning up tickets notifications"))
        self.go_to_main_page()

    def send_ticket_back(self) -> None:
        self.driver.find_element_by_id("hgbar_messages").click()
        try:
            notifications = self.driver.find_elements_by_xpath(
                "//div[@class='tab active']"
                "//div[@class='message daily_draw notification ballot']"
            )
        except NoSuchElementException:
            logger.info(color_green("No raffle tickets to return"))
            return
        for n in notifications:
            self.driver.implicitly_wait(0.3)
            n.find_element_by_class_name("sendBallot").click()
            sleep(0.5)
            # Daily limit reached
            try:
                err_msg = n.find_element_by_class_name("error")
                if "You have already entered" in err_msg.text:
                    pass
                else:
                    logger.info(color_green("Daily limit reached"))
                    self.driver.implicitly_wait(5)
                    break
            except NoSuchElementException:
                pass
        logger.info(color_green("Finished resending raffle tickets"))
        self.driver.implicitly_wait(5)
        self.go_to_main_page()

    def send_ticket_to_recently_active(self) -> None:
        # click on friend
        self.driver.find_elements_by_class_name("mousehuntHud-menu-item")[
            5
        ].click()
        tickets = self.driver.find_elements_by_class_name("sendTicket")
        for t in tickets:
            sleep(0.250)
            t.click()
        logger.info(color_green("Finished sending raffle tickets"))
        self.go_to_main_page()

    def send_gift_to_recently_active(self) -> None:
        # click on friend
        self.driver.find_elements_by_class_name("mousehuntHud-menu-item")[
            5
        ].click()
        tickets = self.driver.find_elements_by_class_name("sendGift")
        for t in tickets:
            sleep(0.250)
            t.click()
        logger.info(color_green("Finished sending raffle tickets"))
        self.go_to_main_page()

    def send_free_gift(self) -> None:
        sleep(1)
        # click on gift
        self.driver.find_element_by_id("hgbar_freegifts").click()
        sleep(1)

        # click on view more
        self.driver.find_element_by_class_name(
            "giftSelectorView-inbox-footer-viewMore"
        ).click()
        sleep(1)

        # click on send free gifts
        self.driver.find_elements_by_class_name("giftSelectorView-tabHeader")[
            1
        ].click()
        sleep(1)

        # select gift of the day
        self.driver.find_elements_by_class_name("gift_of_the_day")[1].click()
        sleep(1)

        favorites = self.driver.find_elements_by_xpath(
            "//a[@class='giftSelectorView-friend favorite']"
        )
        for f in favorites:
            sleep(0.250)
            f.click()
        try:
            send_gift_button = self.driver.find_element_by_xpath(
                "//div[@class='giftSelectorView-content-viewState selectFriends']"  # noqa: E501 pylint: disable=C0301
                "//a[@class='mousehuntActionButton giftSelectorView-action-confirm small']"  # noqa: E501 pylint: disable=C0301
            )
            send_gift_button.click()
        except NoSuchElementException:
            logger.info(color_red("Daily gifts was already send"))
            pass
        self.go_to_main_page()
        logger.info(color_green("Finished sending daily gifts"))

    def collect_dailies(self) -> None:
        sleep(1)
        # click on gift
        self.driver.find_element_by_id("hgbar_freegifts").click()
        sleep(1)

        # click on view more
        self.driver.find_element_by_class_name(
            "giftSelectorView-inbox-footer-viewMore"
        ).click()
        sleep(1)

        # click on send free gifts
        self.driver.find_elements_by_class_name("giftSelectorView-tabHeader")[
            1
        ].click()
        sleep(1)

        gift_of_the_day = (
            self.driver.find_elements_by_class_name("gift_of_the_day")[1]
            .find_elements_by_class_name("giftSelectorView-gift-name")[0]
            .text
        )
        logger.info(f"Gift of the day is {gift_of_the_day}.")

        self.go_to_main_page()
        sleep(1)
        self.driver.find_element_by_id("hgbar_freegifts").click()
        sleep(1)

        gifts = self.driver.find_elements_by_class_name(
            "giftSelectorView-inbox-giftRow"
        )

        for g in gifts:
            if gift_of_the_day in g.text:
                g.find_element_by_class_name("claim").click()
                sleep(0.5)

        self.go_to_main_page()
        logger.info(color_green(f"Finished collecting {gift_of_the_day}"))

    def recover_from_kings_reward(self) -> None:
        while self.has_king_reward:
            self.refresh()
            noise = 2700 + random.randint(60, 900)
            logger.info(
                color_red(
                    f"Kings Reward! Please solve the puzzle. Refresh left = "
                    f"{REFRESH_QUOTA - self.num_refresh}. I will be back in "
                    f"{noise} seconds"
                )
            )
            sleep(noise)
