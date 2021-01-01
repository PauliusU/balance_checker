import datetime

from data import db_connection
from models.balance import Balance


def create_or_update_balance(balance_amount: float, platform_name: str) -> Balance:
    session = db_connection.create_db_session()

    date_of_today: str = datetime.datetime.today().strftime('%Y-%m-%d')  # E.g. "2021-01-01"

    # get balance if exists
    balance = session.query(Balance). \
        filter(Balance.platform_name == platform_name, Balance.date == date_of_today).first()

    # Update balance, if found
    if balance:
        balance.balance = balance_amount
        session.commit()
    # Crete new balance, otherwise
    else:
        balance = Balance()
        balance.platform_name = platform_name
        balance.balance = balance_amount
        balance.date = date_of_today

        session.add(balance)
        session.commit()

        balance = session.query(Balance) \
            .filter(Balance.platform_name == platform_name, Balance.date == date_of_today) \
            .first()

    session.close()
    return balance


def get_balances_of_today():
    session = db_connection.create_db_session()
    date_of_today: str = datetime.datetime.today().strftime('%Y-%m-%d')  # E.g. "2021-01-01"

    balances_bondora = session.query(Balance).filter(Balance.date == date_of_today).all()
    for balance in balances_bondora:
        print(f"{balance.date} {balance.platform_name} {balance.balance}")

    session.close()


if __name__ == '__main__':
    get_balances_of_today()
