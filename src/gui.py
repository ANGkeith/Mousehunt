# Third Party Library
from selenium import webdriver

# My Libary
from MyBot.bot import sign_in

driver = webdriver.Firefox()
driver.implicitly_wait(5)

sign_in(driver)
