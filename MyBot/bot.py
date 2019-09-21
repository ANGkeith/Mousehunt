# Standard Library
import importlib
from time import sleep
from dataclasses import dataclass

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from MyBot.utils import to_lower_case_with_underscore


@dataclass
class Bot:
    driver: webdriver
    horncount: int = 0

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

    def sound_horn(self) -> None:
        hunters_horn = self.driver.find_elements_by_class_name(
            "mousehuntHud-huntersHorn"
        )[0]
        if hunters_horn.location != {"x": 0, "y": 0}:
            hunters_horn.click()
            self.horncount += 1
        else:
            return

    def has_king_reward(self) -> bool:
        try:
            len(self.driver.find_elements_by_class_name("warning")) > 0
        except WebDriverException:
            return False
        return (
            len(self.driver.find_elements_by_class_name("warning")) > 0
            and self.driver.find_elements_by_class_name("warning")[
                0
            ].get_attribute("innerText")
            == "The King wants to give you a reward!"
        )

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
        location = to_lower_case_with_underscore(self.get_location())
        try:
            module = importlib.import_module(f"MyBot.environments.{location}")
            prepare = getattr(module, "prepare")
            prepare(self)
        except ModuleNotFoundError:
            pass
