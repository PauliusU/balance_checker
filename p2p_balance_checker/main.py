import traceback

from data import database_abstraction_layer
import api_bondora
import clean_outputs
import config
import platform_settings
import scraper


def get_platform_balance(platform_name: str) -> float:
    platform_balance: float = 0

    try:
        # Bondora has public API, no scraping is needed
        if platform_name == "Bondora":
            platform_balance: float = api_bondora.get_bondora_balance()
            database_abstraction_layer.create_or_update_balance(
                platform_balance, platform_name)
            return platform_balance  # stop rest try block from executing

        platform: dict = platform_settings.get_platform_settings(platform_name)

        inner_html: str = \
            scraper.get_inner_html_after_login(config.DRIVER_PATH,
                                               platform["url_login"],
                                               platform["element_user"],
                                               platform["element_password"],
                                               platform["username"],
                                               platform["password"],
                                               platform["url_dashboard"],
                                               platform_name)

        html_tag: str = \
            clean_outputs.get_html_tag_from_inner_html(inner_html,
                                                       platform[
                                                           "element_balance"])
        platform_balance: float = clean_outputs.get_float_from_html_tag(
            html_tag)
        database_abstraction_layer.create_or_update_balance(platform_balance,
                                                            platform_name)

        return platform_balance

    except Exception as exception_message:
        print(f"FAILURE: {exception_message}")
        traceback.print_exc()

    finally:
        print(f"{platform_name}: {platform_balance} EUR")
        return platform_balance
