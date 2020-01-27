# Third Party Library
# Standard Library
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# My Libary
from MyBot.bot import sign_in

driver = webdriver.Firefox()
driver.implicitly_wait(5)

sign_in(driver)

while True:
    try:
        driver.window_handles
        sleep(10)
    except WebDriverException:
        break
