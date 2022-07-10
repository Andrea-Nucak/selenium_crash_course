import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
import sys
import os
import time
import definitions

# REPORTING CONSTANTS
SCREENSHOT_DIR = definitions.ROOT_DIR + "/screenshots/"
REPORTS_DIR = definitions.ROOT_DIR + "/reports/"
REPORT_NAME = "Infinum_Web_Regression_Test"

# ENVIRONMENTS
DEV = "dev"
PROD = "prod"

# ENVIRONMENT CONSTANTS
URLS = {
    DEV: "https://beta.infinum.com",
    PROD: "https://infinum.com"
}

# DRIVER CONSTANTS
DRIVER_TIMEOUT = 30


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--env", action="store", default="dev")


@pytest.hookimpl
def pytest_configure(config):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    report_name = REPORT_NAME + "_" + timestamp + ".html"
    config.option.htmlpath = REPORTS_DIR + report_name


@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    return browser


@pytest.fixture
def environment(request):
    environment = request.config.getoption("--env")
    return environment


@pytest.fixture(scope="function")
def driver(browser):
    if browser == "chrome":
        driver = webdriver.Chrome()
        driver.maximize_window()

    elif browser == "chrome-headless":
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

    elif browser == "firefox":
        firefox_service = Service(executable_path="geckodriver", log_path=os.devnull)
        driver = webdriver.Firefox(service=firefox_service)
        driver.maximize_window()

    elif browser == "safari":
        driver = webdriver.Safari()
        driver.maximize_window()

    elif browser == "edge":
        driver = webdriver.Edge()
        driver.maximize_window()

    else:
        sys.exit("Browser not supported!")

    yield driver

    driver.quit()


def pytest_html_report_title(report):
    report.title = REPORT_NAME
