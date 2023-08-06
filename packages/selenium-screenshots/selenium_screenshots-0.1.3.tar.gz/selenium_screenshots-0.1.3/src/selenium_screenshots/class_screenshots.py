"""Main file of this python package with the class Screenshots"""
# Standard library imports
import os
import logging

# Third party imports
from tqdm import tqdm
from local_simple_database import LocalSimpleDatabase
from char import char

# Local imports
from .exceptions import SeleniumScreenshotsError
from .additional import delete_from_file_name_forbidden_characters


LOGGER = logging.getLogger("selenium_screenshots")


class Screenshots(object):
    """Class to handle creation of many screenshots for selenium

    Raises:
        SeleniumScreenshotsError: Main Exception of this python package
    """

    @char
    def __init__(
            self,
            webdriver,
            str_path_dir_with_screenshots="screenshots",
            int_screenshots_to_delete_half=9999,
            int_max_length_of_filename=50,
    ):
        """Init object for handling screenshots

        Args:
            webdriver (selenium.webdriver): Selenium Webdriver
            str_path_dir_with_screenshots (str, optional): \
                Path to directory where to save screenshots.
            int_screenshots_to_delete_half (int, optional): Number of the \
                screenshots in the directory when delete half of them
            int_max_length_of_filename (int, optional): \
                Max length of the filename for new screenshot file
        """
        self.webdriver = webdriver
        self.str_path_dir_with_screenshots = \
            os.path.abspath(str_path_dir_with_screenshots)
        self.LSD = LocalSimpleDatabase(self.str_path_dir_with_screenshots)
        self.int_screenshots_to_delete_half = int_screenshots_to_delete_half
        self.int_max_length_of_filename = int_max_length_of_filename
        # Create directory for the screenshots
        if not os.path.exists(str_path_dir_with_screenshots):
            os.makedirs(str_path_dir_with_screenshots)
            LOGGER.info(
                "Created directory for the screenshots: %s",
                str_path_dir_with_screenshots
            )
        self.LSD["int_screenshots_in_the_dir"] = \
            self._count_screenshots_in_the_directory()

    @char
    def create_screenshot(self, str_description=""):
        """Create a new screenshot with given description

        Args:
            str_description (str): description to add in the screenshot name.

        Raises:
            SeleniumScreenshotsError: Main exception of this python package
        """
        str_filename = self._create_name_for_screenshot(str_description)
        str_screenshot_path = os.path.join(
            self.str_path_dir_with_screenshots, str_filename)
        LOGGER.debug("Create screenshot in path: %s", str_screenshot_path)
        #####
        # Try to create screenshot
        try:
            self.webdriver.get_screenshot_as_file(str_screenshot_path)
        except Exception as ex:
            LOGGER.error(
                "Unable to create screenshot with name: %s", str_filename)
            raise SeleniumScreenshotsError(str(ex))
        self.LSD["int_last_screenshot_num"] += 1
        self.LSD["int_screenshots_in_the_dir"] += 1
        # Delete screenshots if there are too many of them
        if self.LSD["int_screenshots_in_the_dir"] > \
        self.int_screenshots_to_delete_half:
            self._remove_old_screenshots_if_there_are_too_much()

    @char
    def delete_all_screenshots(self):
        """Delete all screenshots in the dir
        """
        list_screens_names = self._get_names_of_all_screenshots()
        LOGGER.info(
            "Delete all screenshots in the directory: %s",
            self.str_path_dir_with_screenshots
        )
        LOGGER.info("---> Screenshots to delete: %d", len(list_screens_names))
        self._delete_list_of_screenshots(list_screens_names)
        # Save new number of screenshots in the dir
        self._update_number_of_screenshots_in_the_dir()

    @char
    def delete_not_unique_screenshots(
            self,
            is_to_delete_screenshots_without_description=False
    ):
        """This method will delete all not unique screenshots in the directory.

        Args:
            is_to_delete_screenshots_without_description (bool, optional): \
                Flag if to delete screenshots without description.
        """
        list_screens_names = self._get_names_of_all_screenshots()
        # Save descriptions of screens by name in the dictionary
        dict_screen_name_by_screen_descr = {}
        list_screens_without_description = []

        for str_screen_name in list_screens_names:
            if "_" not in str_screen_name:
                list_screens_without_description.append(str_screen_name)
                continue
            str_screen_descr = str_screen_name.replace(".png", "")
            # delete screenshot number from screenshot description
            str_screen_descr = "_".join(str_screen_descr.split("_")[1:])
            dict_screen_name_by_screen_descr[str_screen_descr] = \
                str_screen_name
        # Delete not unique screens
        set_unique_screens_descr = set(dict_screen_name_by_screen_descr)
        list_names_unique_screens = [
            dict_screen_name_by_screen_descr[str_unique_descr]
            for str_unique_descr in set_unique_screens_descr
        ]
        if not is_to_delete_screenshots_without_description:
            list_names_unique_screens += list_screens_without_description
        set_screens_names_to_delete = \
            set(list_screens_names) - set(list_names_unique_screens)

        self._delete_list_of_screenshots(list(set_screens_names_to_delete))
        # Save new number of screenshots in the dir
        self._update_number_of_screenshots_in_the_dir()

    @char
    def _delete_list_of_screenshots(self, list_screenshots_names_to_del):
        """Delete list of screenshots from the directory

        Args:
            list_screenshots_names_to_del (list): Names of screenshots
        """
        iter_screens_names = list_screenshots_names_to_del
        if len(list_screenshots_names_to_del) > 1000:
            iter_screens_names = tqdm(iter_screens_names)
        for str_screen_name in iter_screens_names:
            str_screenshot_path = os.path.join(
                self.str_path_dir_with_screenshots, str_screen_name)
            if not os.path.exists(str_screenshot_path):
                continue
            try:
                os.remove(str_screenshot_path)
            except Exception as ex:
                LOGGER.warning(
                    "Unable to delete screenshot: %s\n%s",
                    str_screenshot_path, ex)

    @char
    def _create_name_for_screenshot(self, str_description):
        """Create name for the new screenshot like "<number>_<description>"

        Args:
            str_description (str): string which to add in screenshot name

        Returns:
            str: Name for the screenshot
        """
        # Get number for new screenshot
        int_new_screenshot_num = self.LSD["int_last_screenshot_num"] + 1
        LOGGER.debug("Number for new screenshot: %d", int_new_screenshot_num)
        str_filename = str(int_new_screenshot_num)
        if str_description:
            str_filename += "_" + str_description
        # If the filename is too long then cut it
        if len(str_filename) > self.int_max_length_of_filename:
            str_filename = str_filename[:self.int_max_length_of_filename]
        # Delete forbidden characters
        str_filename_filtered = \
            delete_from_file_name_forbidden_characters(str_filename)
        LOGGER.debug(
            "Created a name for new screenshot: %s", str_filename_filtered)
        return str_filename_filtered + ".png"

    def _remove_old_screenshots_if_there_are_too_much(self):
        """Delete most old screenshots if there are too much of them
        """
        # Check if there are too much screenshots
        list_screens_names = self._get_names_of_all_screenshots()
        if len(list_screens_names) < self.int_screenshots_to_delete_half:
            self.LSD["int_screenshots_in_the_dir"] = len(list_screens_names)
            return None
        # Create dictionary {screenshot_num: screenshot_filename, ...}
        dict_screen_name_by_num = {}
        for str_screenshot_name in list_screens_names:
            try:
                int_screen_num = int(str_screenshot_name.split("_")[0])
            except ValueError:
                LOGGER.warning(
                    "Wrong filename of the screenshot: %s",
                    str_screenshot_name
                )
                continue
            dict_screen_name_by_num[int_screen_num] = str_screenshot_name
        # Create sorted list with screenshot's numbers
        list_sorted_screenshot_numbers = sorted(dict_screen_name_by_num)
        int_screens_to_delete = self.int_screenshots_to_delete_half // 2
        int_screens_deleted = 0
        # Delete old screenshots
        for int_screen_num_to_del in  \
        list_sorted_screenshot_numbers[:int_screens_to_delete]:
            str_screen_name = dict_screen_name_by_num[int_screen_num_to_del]
            str_screenshot_path = os.path.join(
                self.str_path_dir_with_screenshots, str_screen_name)
            LOGGER.debug("Delete screenshot: %s", str_screen_name)
            try:
                os.remove(str_screenshot_path)
                int_screens_deleted += 1
            except OSError:
                LOGGER.warning(
                    "Unable to delete screenshot: %s", str_screenshot_path)
        LOGGER.info("Were deleted screenshots: %d", int_screens_to_delete)
        #####
        # Save new number of screenshots in the dir
        self._update_number_of_screenshots_in_the_dir()
        return None

    def _get_names_of_all_screenshots(self):
        """Get list with names of all screenshots

        Returns:
            list: Names of all screenshots
        """
        list_screenshots_names = [
            filename
            for filename in os.listdir(self.str_path_dir_with_screenshots)
            if ".png" in filename
        ]
        return list_screenshots_names

    def _count_screenshots_in_the_directory(self):
        """Count number of screenshots in the set directory

        Returns:
            int: Number of the screenshots
        """
        return len(self._get_names_of_all_screenshots())

    def _update_number_of_screenshots_in_the_dir(self):
        """Save new number of the screenshots in the dirs
        """
        list_screens_names = self._get_names_of_all_screenshots()
        self.LSD["int_screenshots_in_the_dir"] = len(list_screens_names)
