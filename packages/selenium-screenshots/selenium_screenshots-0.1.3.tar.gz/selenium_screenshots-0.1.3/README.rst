====================
selenium_screenshots
====================


.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/selenium_screenshots
   :target: https://img.shields.io/github/last-commit/stas-prokopiev/selenium_screenshots
   :alt: GitHub last commit

.. image:: https://img.shields.io/github/license/stas-prokopiev/selenium_screenshots
    :target: https://github.com/stas-prokopiev/selenium_screenshots/blob/master/LICENSE.txt
    :alt: GitHub license<space><space>

.. image:: https://readthedocs.org/projects/selenium_screenshots/badge/?version=latest
    :target: https://selenium_screenshots.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/stas-prokopiev/selenium_screenshots.svg?branch=master
    :target: https://travis-ci.org/stas-prokopiev/selenium_screenshots

.. image:: https://img.shields.io/pypi/v/selenium_screenshots
   :target: https://img.shields.io/pypi/v/selenium_screenshots
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/selenium_screenshots
   :target: https://img.shields.io/pypi/pyversions/selenium_screenshots
   :alt: PyPI - Python Version


.. contents:: **Table of Contents**

Short Overview.
=========================
selenium_screenshots is a python package that helps to create many screenshots for selenium webdrivers.

Example
------------------------------

.. code-block:: python

    from selenium import webdriver
    from selenium_screenshots import make_screenshot
    # Please define here any webdriver which you would like to use E.G. driver = webdriver.Chrome()
    # When you would want to create a screenshot, just call
    make_screenshot(driver)
    make_screenshot(driver, "some_description")
    make_screenshot(driver, "characters_%%forbidden_in_the_..filename")

As the result you will get screenshots in the directory: **./screenshots/...**

- 1.png
- 2_some_description.png
- 3_characters___forbidden_in_the___filename.png

If you run this code some other time then you'll get 3 more screenshots:

- 1.png
- 2_some_description.png
- 3_characters___forbidden_in_the___filename.png
- 4.png
- 5_some_description.png
- 6_characters___forbidden_in_the___filename.png

As you can see user shouldn't worry about screenshot's numbers as they will be handled automatically.

Installation via pip:
======================

.. code-block:: bash

    pip install selenium_screenshots

Basic Usage
=========================

Full signature of selenium_screenshots.make_screenshot(...)
--------------------------------------------------------------------------------------------------

.. code-block:: python

    from selenium_screenshots import make_screenshot

    make_screenshot(
        webdriver,
        str_description="",
        str_path_dir_with_screenshots="screenshots",
    )

Arguments
^^^^^^^^^^^^^^

#. **webdriver**:
    The only mandatary argument. Any selenium webdriver which to use for making of screenshot.
#. **str_description=""**:
    | Description of the screenshot to add to the screenshot filename.
    | If in the screenshot description will be used symbols forbidden in the filenames they will be replaced on "_".
    | If filename of a new screenshot is longer than 50 symbols then it will be cut to 50.
#. **str_path_dir_with_screenshots="screenshots"**:
    Path to the directory where you want to save a new screenshot

Advanced Usage
=========================

**selenium_screenshots.Screenshots(...)**
--------------------------------------------------------------------------------------------------

| Firstly, you have to define an object of class Screenshots to be able to handle screenshots.
| This object will be named **screenshots_handler** in the code below.

.. code-block:: python

    from selenium import webdriver
    from selenium_screenshots.main import Screenshots

    # Please define here any webdriver which you would like to use E.G. driver = webdriver.Chrome()
    screenshots_handler = Screenshots(
            webdriver,
            str_path_dir_with_screenshots="screenshots",
            int_screenshots_to_delete_half=9999,
            int_max_length_of_filename=50,
    )

Arguments
^^^^^^^^^^^^^^

#. **webdriver**:
    The only mandatary argument. Any selenium webdriver which to use for making of screenshots.
#. **str_path_dir_with_screenshots="screenshots"**:
    Path to directory where to save screenshots.
#. **int_screenshots_to_delete_half=9999**:
    Number of the screenshots in the directory when try to delete most old half
#. **int_max_length_of_filename=50**:
    | Max length of a new screenshot filename.
    | If filename of a new screenshot is longer then filename will be cut.

Methods of **screenshots_handler** object
--------------------------------------------------------------------------------------------------

screenshots_handler.create_screenshot(...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method do exactly the same as **selenium_screenshots.make_screenshot(...)** in the **Basic Usage**

.. code-block:: python

    screenshots_handler.create_screenshot(str_description="")

#. **str_description=""**:
    | Description of the screenshot to add to the screenshot filename.
    | If in the screenshot description is used symbols forbidden in the filenames they will be replaced on "_".
    | If filename of a new screenshot is longer than N symbols then it will be cut to N.

screenshots_handler.delete_all_screenshots(...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This method will delete all screenshots in the directory.
| Max used screenshot number won't be lost, so new screenshot will have next number rather than 1.

.. code-block:: python

    screenshots_handler.delete_all_screenshots()


screenshots_handler.delete_not_unique_screenshots(...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This method will delete screenshots with not unique descriptions.

.. code-block:: python

    screenshots_handler.delete_not_unique_screenshots(
        is_to_delete_screenshots_without_description=False)

#. **is_to_delete_screenshots_without_description=False**:
    | Flag if to delete screenshots without description

How to create screenshot every time when you caught an Exception
---------------------------------------------------------------------------

| You can use this python package to make screenshots for every exception
| with preserved description of an error in the screenshot filename.


.. code-block:: python

    from selenium_screenshots import make_screenshot

    try:
        # Some code which you would like to test
    except Exception as ex:
        make_screenshot(webdriver, str_description=str(ex))
        raise

Links
=====

    * `PYPI <https://pypi.org/project/selenium_screenshots/>`_
    * `readthedocs <https://selenium_screenshots.readthedocs.io/en/latest/>`_
    * `GitHub <https://github.com/stas-prokopiev/selenium_screenshots>`_

Project local Links
===================

    * `CHANGELOG <https://github.com/stas-prokopiev/selenium_screenshots/blob/master/CHANGELOG.rst>`_.
    * `CONTRIBUTING <https://github.com/stas-prokopiev/selenium_screenshots/blob/master/CONTRIBUTING.rst>`_.

Contacts
========

    * Email: stas.prokopiev@gmail.com
    * `vk.com <https://vk.com/stas.prokopyev>`_
    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.

