from base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):

    slug = ""
    blog_navigation_button_locator = (By.XPATH, "//span[text()='Blog']")

    def navigate_to_page(self):
        self.navigate(self.slug)

    @property
    def blog_navigation_button(self):
        return self.get_present_element(self.blog_navigation_button_locator)
