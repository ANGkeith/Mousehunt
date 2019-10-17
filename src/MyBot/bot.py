# Standard Library
import sys
import random
import logging
import importlib
from time import sleep
from dataclasses import field, dataclass

from selenium import webdriver
from MyBot.utils import (
    play_sound,
    log_identifier,
    noise_generator,
    is_sleeping_time,
    to_lower_case_with_underscore,
)
from MyBot.settings import URL, NORMAL_DELAY, NIGHT_TIME_DELAY
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)


@dataclass
class Bot:
    driver: webdriver = field(init=False)
    horncount: int = 0
    refresh: int = 0

    def __post_init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(15)
        self.driver.get(URL)
        self.sign_in(sys.argv[1], sys.argv[2])

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
        if self.has_king_reward():
            play_sound()
            logging.info(
                f"{log_identifier()} Kings Reward! Please help me to solve the "
                f"puzzle, I will be back in {NORMAL_DELAY} seconds"
            )
            sleep(NORMAL_DELAY)
        elif self.is_ready():
            # wait for random amount of time before sounding horn again
            noise = noise_generator()
            logging.info(
                f"{log_identifier()} Horn is ready, Sounding horn in "
                f"{noise} seconds"
            )
            sleep(noise)
            self.sound_horn()
        else:
            self.prepare()
            logging.info(
                f"{log_identifier()} Horn is not ready yet, still has "
                f"{self.get_time_left()} to go. (Number of horn sounded so "
                f"far: {self.horncount})"
            )
            if is_sleeping_time():
                noise = NIGHT_TIME_DELAY + random.randint(600, 1200)
                logging.info(
                    f"{log_identifier()}. It is currently night time. Waiting "
                    f"for {noise} seconds"
                )
                sleep(noise)
            else:
                logging.info(
                    f"{log_identifier()} Waiting for {NORMAL_DELAY} seconds"
                )
                sleep(NORMAL_DELAY)

    def sound_horn(self) -> None:
        hunters_horn = self.driver.find_elements_by_class_name(
            "mousehuntHud-huntersHorn"
        )[0]
        try:
            hunters_horn.click()
            self.horncount += 1
            logging.info(
                f"{log_identifier()} Horn is sounded, taking a break for 13 "
                "minutes"
            )
            sleep(780)

        except ElementClickInterceptedException:
            if self.refresh < 3:
                self.driver.refresh()
                self.refresh += 1
                logging.info(
                    f"{log_identifier()} Horn image is intercepted, attempting "
                    f"to relaunch browser. (Retries left: {3 - self.refresh}"
                )
            else:
                logging.error(
                    f"{log_identifier()} Refreshed too many times, good bye"
                )
                sys.exit(1)

        except Exception as e:
            logging.error(f"{log_identifier()} {e}")
            sys.exit(1)

    def has_king_reward(self) -> bool:
        try:
            return (
                len(self.driver.find_elements_by_class_name("warning")) > 0
                and self.driver.find_elements_by_class_name("warning")[
                    0
                ].get_attribute("innerText")
                == "The King wants to give you a reward!"
            )
        except NoSuchElementException:
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
