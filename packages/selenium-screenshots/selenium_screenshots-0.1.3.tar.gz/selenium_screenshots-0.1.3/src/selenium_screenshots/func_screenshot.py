"""Main file of this python package with the class Screenshots"""
# Standard library imports
import logging

# Third party imports
from char import char

# Local imports
from .class_screenshots import Screenshots


LOGGER = logging.getLogger("selenium_screenshots")


@char
def make_screenshot(
        webdriver,
        str_description="",
        str_path_dir_with_screenshots="screenshots",
):
    """Create a screenshot without initializing a class obj

    Args:
        webdriver (selenium.webdriver): \
            webdriver which to use for creation of screenshot
        str_description (str, optional): \
            Additional description of the screenshot
        str_path_dir_with_screenshots (str, optional): \
            Path to directory where to save screenshot
    """
    screenshot_obj = Screenshots(
        webdriver,
        str_path_dir_with_screenshots=str_path_dir_with_screenshots
    )
    screenshot_obj.create_screenshot(str_description=str_description)
