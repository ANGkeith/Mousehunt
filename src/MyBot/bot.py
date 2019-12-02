# Standard Library
import sys
import logging
import importlib
from time import sleep
from datetime import datetime
from dataclasses import field, dataclass

from environs import Env
from selenium import webdriver
from MyBot.utils import (
    set_env,
    color_red,
    play_sound,
    color_green,
    log_identifier,
    noise_generator,
    get_latest_journal_entry,
    to_lower_case_with_underscore,
)
from MyBot.settings import URL, ENV_DAILIES, NORMAL_DELAY
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
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


@dataclass
class Bot:
    env: Env = field(init=False)
    driver: webdriver = field(init=False)
    horncount: int = 0
    num_refresh: int = 0

    def __post_init__(self) -> None:
        self.env = Env()
        self.env.read_env()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get(URL)
        self.sign_in(self.env("username"), self.env("password"))

    def sign_in(self, username: str, password: str) -> None:
        # click on Sign in
        sleep(1.5)
        self.driver.find_elements_by_class_name("signInText")[0].click()

        # Enter credentials
        elem = self.driver.find_elements_by_class_name("username")[3]
        elem.send_keys(username)
        elem = self.driver.find_elements_by_class_name("password")[3]
        sleep(5)
        elem.send_keys(password)

        # Click Login
        elem = self.driver.find_elements_by_class_name("actionButton")[
            1
        ].click()

    def start(self) -> None:
        self.env.read_env(override=True)
        if self.env.bool(ENV_DAILIES, False):
            self.resend_ticket()
            self.send_free_gift()
            self.go_to_main_page()
            set_env(ENV_DAILIES, "True", "False")
        if self.has_king_reward():
            play_sound()
            logger.info(
                color_red(
                    f"{log_identifier()} Kings Reward! Please help me to solve "
                    f"the puzzle, I will be back in {NORMAL_DELAY} seconds"
                )
            )
            sleep(NORMAL_DELAY)
        elif self.is_ready():
            # wait for random amount of time before sounding horn again
            noise = noise_generator()
            logger.info(
                f"{log_identifier()} Horn is ready, Sounding horn in "
                f"{noise} seconds"
            )
            sleep(noise)
            self.sound_horn()

        else:
            self.prepare()
            logger.info(
                f"{log_identifier()} Horn is not ready yet, still has "
                f"{self.get_time_left()} to go. (Number of horn sounded so "
                f"far: {self.horncount})"
            )
            sleep(NORMAL_DELAY)

    def sound_horn(self) -> None:
        hunters_horn = self.driver.find_elements_by_class_name(
            "mousehuntHud-huntersHorn"
        )[0]
        try:
            hunters_horn.click()
            self.horncount += 1
            logger.info(
                color_green(
                    f"{log_identifier()} Horn is sounded, taking a break for "
                    "12 minutes"
                )
            )
            if "Treasure Map Clue" in get_latest_journal_entry(self):
                logger.info(color_green("Found Treasure Map Clue"))
                play_sound()
            for i in range(12):
                sleep(NORMAL_DELAY)
                if int(datetime.now().strftime("%M")) == 45:
                    logger.debug(f"{log_identifier()} refreshing")
                    self.go_to_main_page()
                    break
        except ElementClickInterceptedException:
            self.refresh()
        except ElementNotInteractableException:
            self.refresh()
        except Exception as e:
            logger.error(color_red(f"{log_identifier()} {e}"))
            sys.exit(1)

    def refresh(self) -> None:
        if self.num_refresh < 3:
            self.driver.refresh()
            self.num_refresh += 1
            logger.warning(
                color_red(
                    f"{log_identifier()} Horn image is intercepted, attempting "
                    f"to relaunch browser. (Retries left: "
                    f"{3 - self.num_refresh}"
                )
            )
        else:
            logger.error(
                color_red(
                    f"{log_identifier()} Refreshed too many times, good bye"
                )
            )
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

    def go_to_main_page(self) -> None:
        self.driver.get(URL)

    def resend_ticket(self) -> None:
        """
        Send ticket from notification
        """
        self.driver.find_element_by_id("hgbar_messages").click()
        notifications = self.driver.find_elements_by_xpath(
            "//div[@class='tab active']"
            "//div[@class='message daily_draw notification ballot']"
        )
        for n in notifications:
            n.find_element_by_class_name("sendBallot").click()
            sleep(0.5)

    def send_ticket(self) -> None:
        """
        Send ticket to recently active friend
        """
        # click on friend
        self.driver.find_elements_by_class_name("mousehuntHud-menu-item")[
            5
        ].click()
        tickets = self.driver.find_elements_by_class_name("sendTicket")
        for t in tickets:
            sleep(0.250)
            t.click()
        sleep(1)
        logger.info(color_green("Finished sending raffle tickets"))

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
                "//div[@class='giftSelectorView-content-viewState selectFriends']"
                "//a[@class='mousehuntActionButton giftSelectorView-action-confirm small']"
            )
            send_gift_button.click()
        except NoSuchElementException:
            logger.info(color_red("Daily gifts was already send"))
            pass
        logger.info(color_green("Finished sending daily gifts"))
