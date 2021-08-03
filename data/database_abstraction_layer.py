import datetime
from sqlalchemy.sql import func

from data import db_connection
from models.balance import Balance


def create_or_update_balance(balance_amount: float,
                             platform_name: str) -> Balance:
    session = db_connection.create_db_session()

    # E.g. "2021-01-01"
    date_of_today: str = datetime.datetime.today().strftime('%Y-%m-%d')

    # get balance if exists
    balance = session.query(Balance). \
        filter(Balance.platform_name == platform_name,
               Balance.date == date_of_today).first()

    # Update balance, if found
    if balance:
        balance.balance = balance_amount
        balance.updated_at = get_time_date_string()
        session.commit()
    # Crete new balance, otherwise
    else:
        balance = Balance()
        balance.platform_name = platform_name
        balance.balance = balance_amount
        balance.date = date_of_today
        balance.created_at = get_time_date_string()

        session.add(balance)
        session.commit()

        balance = session.query(Balance) \
            .filter(Balance.platform_name == platform_name,
                    Balance.date == date_of_today) \
            .first()

    session.close()
    return balance


def get_balances_of_today() -> list:
    session = db_connection.create_db_session()
    date_of_today: str = datetime.datetime.today().strftime(
        '%Y-%m-%d')  # E.g. "2021-01-01"

    balances_of_today = session.query(Balance).filter(
        Balance.date == date_of_today).all()
    for balance in balances_of_today:
        print(f"{balance.date} {balance.platform_name} {balance.balance}")

    session.close()

    return list(balances_of_today)


def get_last_daily_balance() -> None:
    session = db_connection.create_db_session()

    total_amount = session.query(Balance.date, func.sum(Balance.balance).label(
        "daily_balance")) \
        .group_by(Balance.date) \
        .order_by(Balance.date.desc()) \
        .first()

    print(
        f"{total_amount.date} LAST DAILY TOTAL: "
        f"{round(total_amount.daily_balance, 2)}")

    session.close()


def get_time_date_string() -> str:
    """ Get ISO8601 date and time string ("YYYY-MM-DD HH:MM:SS.SSS")
    Helper function used for for "created_at" and "updated_at" fields
    """
    return str(
        datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds'))
