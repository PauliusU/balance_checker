from typing import Optional

import api_bondora
import clean_outputs
import platform_settings
import scraper

chrome_driver_path: str = r"..\bin\chromedriver.exe"


def get_platform_balance(platform_name: str) -> float:
    platform_balance: float = 0

    try:
        if platform_name == "Bondora":
            platform_balance = api_bondora.get_bondora_balance()
            return platform_balance  # stop rest try block from executing

        platform = platform_settings.get_platform_settings(platform_name)
        print(platform)

        inner_html: str = scraper.get_inner_html(chrome_driver_path, platform["url"])
        # print(inner_html)
        # TODO: filter_html
        # html_string: str = inner_html
        # platform_balance: float = clean_outputs.get_float_from_html_string(html_string)
        # write to db

        print(platform_balance)
        return platform_balance
    finally:
        print(f"{platform_name}: {platform_balance} EUR")
        return platform_balance


if __name__ == '__main__':
    # get_platform_balance("Bondora")
    # print("-------------------")
    get_platform_balance("Finbee")
