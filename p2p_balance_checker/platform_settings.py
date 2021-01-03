import dotenv
import json
import os

import config

dotenv.load_dotenv()  # get environment variables from .env file


def get_platform_settings(platform_name) -> dict:
    """Get dictionary of both public and private settings for platform"""

    # Get public settings
    with open(config.PLATFORM_SETTINGS_PATH, 'r') as json_file:
        parsed_json: dict = json.load(json_file)

    platform_settings: dict = parsed_json[platform_name]

    # Add private settings from .env file
    platform_settings["username"] = os.getenv(f"{platform_name.upper()}_USERNAME")
    platform_settings["password"] = os.getenv(f"{platform_name.upper()}_PASSWORD")

    return platform_settings
