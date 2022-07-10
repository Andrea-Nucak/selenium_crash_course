from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from pytest_html import extras
from logging import info
import conftest
import time
import sys


class BasePage:
    def __init__(self, driver: WebDriver, environment):
        self.driver = driver
        self.environment = environment

    # NAVIGATION

    def navigate(self, url_slug):
        if self.environment in conftest.URLS.keys():
            base_url = conftest.URLS[self.environment]
            self.driver.get(base_url + url_slug)
        else:
            sys.exit("Environment not defined!")

    # FETCHING

    def get_present_element(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        condition = expected_conditions.presence_of_element_located
        return self.__get_element(locator_value, condition, timeout)

    def get_visible_element(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        condition = expected_conditions.visibility_of_element_located
        return self.__get_element(locator_value, condition, timeout)

    def get_invisible_element(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        condition = expected_conditions.invisibility_of_element_located
        return self.__get_element(locator_value, condition, timeout)

    def get_present_elements(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        condition = expected_conditions.presence_of_all_elements_located
        return self.__get_elements(locator_value, condition, timeout)

    # FETCHING - PRIVATE

    def __get_element(self, locator_value, expected_condition, timeout):
        locator = locator_value[0]
        value = locator_value[1]
        condition = expected_condition

        try:
            element: WebElement = WebDriverWait(self.driver, timeout).until(condition((locator, value)))
            return element

        except Exception:
            info("Getting {} failed".format(value))

    def __get_elements(self, locator_value, expected_condition, timeout):
        locator = locator_value[0]
        value = locator_value[1]
        condition = expected_condition

        try:
            elements: [WebElement] = WebDriverWait(self.driver, timeout).until(condition((locator, value)))
            return elements

        except Exception:
            info("Getting {} failed".format(value))

    # WAITING

    def wait_until_element_present(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        self.__wait_until(locator_value, expected_conditions.presence_of_element_located, timeout)

    def wait_until_element_visible(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        self.__wait_until(locator_value, expected_conditions.visibility_of_element_located, timeout)

    def wait_until_element_clickable(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        self.__wait_until(locator_value, expected_conditions.element_to_be_clickable, timeout)

    def wait_until_element_invisible(self, locator_value, timeout=conftest.DRIVER_TIMEOUT):
        self.__wait_until(locator_value, expected_conditions.invisibility_of_element_located, timeout)

    def wait_until_title_matches(self, title, timeout=conftest.DRIVER_TIMEOUT):
        condition = expected_conditions.title_is
        WebDriverWait(self.driver, timeout).until(condition(title))

    # WAITING - PRIVATE

    def __wait_until(self, locator_value, expected_condition, timeout):
        locator = locator_value[0]
        value = locator_value[1]
        WebDriverWait(self.driver, timeout).until(expected_condition((locator, value)))

    # VALIDATING

    def is_title_matching(self, expected_title, timeout=conftest.DRIVER_TIMEOUT):
        condition = expected_conditions.title_is

        try:
            WebDriverWait(self.driver, timeout).until(condition(expected_title))
            return True

        except Exception:
            return False

    # INTERACTING

    def hover_over_element(self, element):
        try:
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()

        except Exception:
            info("Hovering on {} failed".format(element))

    def drag_and_drop(self, start_element, end_element):
        try:
            ActionChains(self.driver).click_and_hold(start_element).move_by_offset(10, 0).release(end_element).perform()

        except Exception:
            info("Dragging {} failed".format(start_element))

    # JAVASCRIPT

    def browser_go_back(self):
        try:
            self.driver.execute_script("window.history.go(-1)")

        except Exception:
            info("Going back failed")

    def scroll_to_element(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)

        except Exception:
            info("Scrolling to {} failed".format(element))

    def set_local_storage_key(self, key, value):
        try:
            self.driver.execute_script("window.localStorage.setItem({}, {});".format(key, value))

        except Exception:
            info("Setting local storage key failed")

    def save_screenshot(self, extra):
        timestamp = str(int(time.time()))
        image_name = timestamp + ".png"
        image_path = conftest.SCREENSHOT_DIR + image_name

        try:
            self.driver.save_screenshot(image_path)
            # Appends the screenshot image to the HTML report
            extra.append(extras.image(image_path))

        except Exception:
            info("Saving screenshot failed")
