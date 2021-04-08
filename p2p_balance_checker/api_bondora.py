import os
import time
import traceback
import dotenv  # for getting variables from .env file
import requests

dotenv.load_dotenv()  # get variables from .env file

headers: dict = {'Authorization': os.getenv('BONDORA_AUTHORIZATION')}
bondora_api_url = "https://api.bondora.com/"
bondora_get_balance_url = bondora_api_url + 'api/v1/account/balance'


def get_bondora_balance() -> float:
    # authorise and download JSON
    response: requests.models.Response = requests.get(bondora_get_balance_url,
                                                      headers=headers)

    try:
        if response.status_code == 429:  # if "Too Many Requests"
            data: dict = response.json()
            print(f'Bondora: {data["Errors"][0]["Message"]}')

            retry_after_message: str = data["Errors"][0]["Details"]
            # get number from string e.g. "Retry after 547" >> 547
            retry_after_seconds: int = int(retry_after_message.split()[2])
            print(f"{retry_after_message} seconds "
                  f"[{convert_secs_into_hms(retry_after_seconds)}].")
            return 0
        # Raise `HTTPError`, if one occurred, return None
        elif not response.raise_for_status():
            data: dict = response.json()

            balance_main_account: float = data["Payload"]["TotalAvailable"]
            balance_go_grow_accounts: float = 0
            for account in data["Payload"]["GoGrowAccounts"]:
                balance_go_grow_accounts += account["TotalSaved"]

            balance_total: float = \
                balance_main_account + balance_go_grow_accounts
            # platform_sum = format(balance_total, '.2f')
            #
            # return float(platform_sum)

            return round(balance_total, 2)
    except Exception as exception_message:
        print(f"Bondora: >>>>>>>>>> {exception_message}")
        traceback.print_exc()


def convert_secs_into_hms(seconds: int) -> str:
    """ Convert seconds into hours, minutes and seconds

    gmtime is used to convert seconds to special tuple format that strftime()
    requires.
    """
    return time.strftime("%H:%M:%S", time.gmtime(seconds))
