import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def get_inner_html_after_login(driver_path: str,
                               url_login: str,
                               selector_user_field: str,
                               selector_password_field: str,
                               value_user: str,
                               value_password: str,
                               url_dashboard: str = "",
                               platform_name: str = "") -> str:
    try:
        driver: webdriver.chrome.webdriver.WebDriver = webdriver.Chrome(driver_path)

        # Load a web page in the current browser session.
        driver.get(url_login)

        # LOGIN
        # Find fields. Their type is <webdriver.remote.webelement.WebElement>
        user_field = driver.find_element_by_css_selector(selector_user_field)
        password_field = driver.find_element_by_css_selector(selector_password_field)

        # Fill form and press enter
        user_field.send_keys(value_user)
        password_field.send_keys(value_password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(0.5)

        # Navigate to page
        driver.get(url_dashboard)
        time.sleep(3)  # wait for page to fully load

        # Get inner HTML after successful login
        inner_html: str = driver.execute_script("return document.body.innerHTML")

        driver.close()

        return inner_html

    except TypeError as exception_message:
        print(f"FAILURE: check if .env file includes credentials for {platform_name}")
        traceback.print_exc()

    except Exception as exception_message:
        print(f"FAILURE {platform_name}: {exception_message}")
        traceback.print_exc()
