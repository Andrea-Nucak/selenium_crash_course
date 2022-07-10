import pytest
from logging import info
from pages.blog_page import BlogPage
from pages.home_page import HomePage
import pytest_check as check


class TestBlog:

    @pytest.fixture(scope="function")
    def set_up(self, driver, environment):
        self.blog_page = BlogPage(driver, environment)
        self.home_page = HomePage(driver, environment)

        self.home_page.navigate_to_page()

    # Test with soft asserts
    @pytest.mark.regression
    def test_navigate_to_blog_page(self, set_up, extra):
        info("Navigates to blog posts and verifies that the blog title is correct.")

        self.home_page.blog_navigation_button.click()
        self.blog_page.wait_for_blog_page_to_load()
        self.blog_page.save_screenshot(extra)

        # Soft assert that fails, but the test continues
        check.is_true(self.blog_page.blog_name_label.text == "Random invalid name :) ")

        # Soft assert that passes and after which the test is finished
        check.is_true(self.blog_page.blog_name_label.text == "Typing as we speak")

    # Test with standard Python 'assert'
    @pytest.mark.smoke
    def test_navigate_to_blog_page_second_example(self, set_up, extra):
        info("Navigates to blog posts and verifies that the blog title is correct.")

        self.home_page.blog_navigation_button.click()
        self.blog_page.wait_for_blog_page_to_load()
        self.blog_page.save_screenshot(extra)

        assert self.blog_page.blog_name_label.text == "Typing as we speak"
