# Standard Library
from time import sleep

from MyBot.bot import Bot
from MyBot.utils import color_red, noise_generator
from selenium.common.exceptions import WebDriverException


def main() -> None:
    try:
        myBot = Bot()
    except WebDriverException:
        noise = noise_generator()
        sleep(noise)
        myBot = Bot()

    send_ticket(myBot)
    send_free_gift(myBot)
    print(color_red("Done"))


def send_ticket(myBot: Bot) -> None:
    # click on friend
    myBot.driver.find_elements_by_class_name("mousehuntHud-menu-item")[
        5
    ].click()
    tickets = myBot.driver.find_elements_by_class_name("sendTicket")
    for t in tickets:
        sleep(0.250)
        t.click()
    sleep(1)


def send_free_gift(myBot: Bot) -> None:
    sleep(1)
    # click on gift
    myBot.driver.find_element_by_id("hgbar_freegifts").click()
    sleep(1)

    # click on view more
    myBot.driver.find_element_by_class_name(
        "giftSelectorView-inbox-footer-viewMore"
    ).click()
    sleep(1)

    # click on send free gifts
    myBot.driver.find_elements_by_class_name("giftSelectorView-tabHeader")[
        1
    ].click()
    sleep(1)

    # select gift of the day
    myBot.driver.find_elements_by_class_name("gift_of_the_day")[1].click()
    sleep(1)

    favorites = myBot.driver.find_elements_by_xpath(
        "//a[@class='giftSelectorView-friend favorite']"
    )
    for f in favorites:
        sleep(0.250)
        f.click()
    send_gift_button = myBot.driver.find_element_by_xpath(
        "//div[@class='giftSelectorView-content-viewState selectFriends']"
        "//a[@class='mousehuntActionButton giftSelectorView-action-confirm small']"
    )
    send_gift_button.click()


if __name__ == "__main__":
    main()
