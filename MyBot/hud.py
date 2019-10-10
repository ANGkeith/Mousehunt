from typing import Any


def armCharm(element: Any) -> None:
    """
    Used arm charms from HUD

    :param element: driver.find_elements_by_class_name("charm"[i] where i is the
    index of choice
    """
    if not isArmed(element):
        element.click()


def disArmCharm(element: Any) -> None:
    """
    Used to disarm charm from HUD

    :param element: driver.find_elements_by_class_name("charm"[i] where i is the
    index of choice
    """
    if isArmed(element):
        element.click()


def isArmed(element: Any) -> bool:
    """
    Used to check whether the charm is armed from HUD

    :param element: driver.find_elements_by_class_name("charm"[i] where i is the
    index of choice
    """
    return element.get_attribute("class") == "charm active"
