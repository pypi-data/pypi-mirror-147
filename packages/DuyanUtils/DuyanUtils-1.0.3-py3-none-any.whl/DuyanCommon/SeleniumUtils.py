import time
from enum import Enum

import selenium

from selenium import webdriver
from selenium.webdriver.common.by import By


class CatAction(Enum):
    CLICK = 1
    INPUT = 2
    GET_ELEMENT = 3
    GET_ELEMENTS = 4
    CLEAR = 5
    SUBMIT = 6
    GET_VALUE = 7


class ItemInfo(object):
    def __init__(self, send_value=None, attribute_name=None):
        self.send_value = send_value
        self.attribute_name = attribute_name


class Cat(object):
    def __init__(self, by: By, name: str, action: CatAction, item_info: ItemInfo = None):
        self.by = by
        self.name = name
        self.action = action
        self.item_info = item_info

    def do(self, driver):
        if CatAction.GET_ELEMENTS == self.action:
            return driver.find_elements(self.by, self.name)
        elif CatAction.GET_ELEMENT == self.action:
            return driver.find_element(self.by, self.name)
        elif CatAction.CLICK == self.action:
            driver.find_element(self.by, self.name).click()
            return None
        elif CatAction.INPUT == self.action:
            driver.find_element(self.by, self.name).send_keys(self.item_info.send_value)
            return None
        elif CatAction.CLEAR == self.action:
            driver.find_element(self.by, self.name).clear()
        elif CatAction.SUBMIT == self.action:
            driver.find_element(self.by, self.name).submit()
        elif CatAction.GET_VALUE == self.action:
            if self.item_info.attribute_name == "text":
                return driver.text
            return driver.get_attribute(self.item_info.attribute_name)
        return None


class WebDriver(object):

    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.driver = webdriver.Chrome(executable_path)
        self.driver.maximize_window()
        a = self.driver.find_element().text

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path)
