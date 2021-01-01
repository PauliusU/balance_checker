from selenium import webdriver


def get_inner_html(driver_path: str, url: str, login_required=True) -> str:
    driver = webdriver.Chrome(driver_path)

    # Load a web page in the current browser session.
    driver.get(url)

    if login_required:
        print("login is required")

    inner_html: str = driver.execute_script("return document.body.innerHTML")

    return inner_html


# def get_inner_html_after_login(driver_path: str, url: str) -> str:
#     driver = webdriver.Chrome(driver_path)
#
#     # Load a web page in the current browser session.
#     driver.get(url)
#
#     inner_html: str = driver.execute_script("return document.body.innerHTML")
#
#     return inner_html


if __name__ == '__main__':
    pass
