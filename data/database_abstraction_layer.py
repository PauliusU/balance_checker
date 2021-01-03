import datetime
from sqlalchemy.sql import func

from data import db_connection
from models.balance import Balance
from models.withdrawal import Withdrawal


def create_or_update_balance(balance_amount: float, platform_name: str) -> Balance:
    session = db_connection.create_db_session()

    date_of_today: str = datetime.datetime.today().strftime('%Y-%m-%d')  # E.g. "2021-01-01"

    # get balance if exists
    balance = session.query(Balance). \
        filter(Balance.platform_name == platform_name, Balance.date == date_of_today).first()

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


def get_total_balance_of_today():
    session = db_connection.create_db_session()
    date_of_today: str = datetime.datetime.today().strftime('%Y-%m-%d')  # E.g. "2021-01-01"

    total_amount = session.query(Balance.date, func.sum(Balance.balance).label("daily_balance")) \
        .group_by(Balance.date) \
        .order_by(Balance.date.desc()) \
        .first()

    print(f"{total_amount.date} TOTAL: {round(total_amount.daily_balance, 2)}")

    session.close()


def get_total_balance_by_day():
    session = db_connection.create_db_session()

    total_amounts_by_day = session.query(Balance.date, func.sum(Balance.balance).label("daily_balance")) \
        .group_by(Balance.date) \
        .all()

    for row in total_amounts_by_day:
        print(f"{row.date} {round(row.daily_balance, 2)}")

    session.close()


def create_withdrawal(date: str, platform_name: str, withdrawal_amount: float) -> Withdrawal:
    session = db_connection.create_db_session()

    withdrawal = Withdrawal()
    withdrawal.date = date
    withdrawal.platform_name = platform_name
    withdrawal.withdrawal = withdrawal_amount
    withdrawal.created_at = get_time_date_string()

    session.add(withdrawal)
    session.commit()

    print(f"{type(withdrawal.id)} {withdrawal.id=}")
    withdrawal = session.query(Withdrawal).filter(Withdrawal.id == withdrawal.id).first()
    session.close()

    return withdrawal


def get_time_date_string() -> str:
    """ Get ISO8601 date and time string ("YYYY-MM-DD HH:MM:SS.SSS")
    """
    return str(datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds'))
