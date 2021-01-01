from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def get_inner_html_after_login(driver_path: str,
                               url: str,
                               user_element: str = "",
                               password_element: str = "",
                               user_value: str = "",
                               password_value: str = "",
                               url_dashboard: str = "") -> str:
    driver: webdriver.chrome.webdriver.WebDriver = webdriver.Chrome(driver_path)

    # Load a web page in the current browser session.
    driver.get(url)

    # LOGIN
    # Find fields. Their type is <webdriver.remote.webelement.WebElement>
    user_field = driver.find_element_by_css_selector(user_element)
    password_field = driver.find_element_by_css_selector(password_element)
    # driver.implicitly_wait(60)

    # Fill form and press enter
    user_field.send_keys(user_value)
    password_field.send_keys(password_value)
    password_field.send_keys(Keys.RETURN)

    # Navigate to page
    driver.get(url_dashboard)

    time.sleep(5.0)  # wait for page to fully load

    # Get inner HTML after successful login
    inner_html: str = driver.execute_script("return document.body.innerHTML")

    # driver.quit()
    driver.close()

    return inner_html


if __name__ == '__main__':
    pass
