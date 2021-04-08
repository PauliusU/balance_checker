import datetime
from sqlalchemy.sql import func

from data import db_connection
from models.balance import Balance
from models.withdrawal import Withdrawal


def create_withdrawal(date: str, platform_name: str,
                      withdrawal_amount: float) -> Withdrawal:
    session = db_connection.create_db_session()

    withdrawal = Withdrawal()
    withdrawal.date = date
    withdrawal.platform_name = platform_name
    withdrawal.withdrawal = withdrawal_amount
    withdrawal.created_at = get_time_date_string()

    session.add(withdrawal)
    session.commit()

    print(f"{type(withdrawal.id)} {withdrawal.id=}")
    withdrawal = session.query(Withdrawal).filter(
        Withdrawal.id == withdrawal.id).first()
    session.close()

    return withdrawal


def create_or_update_withdrawal(withdrawal_amount: float,
                                platform_name: str) -> Withdrawal:
    """ Negative (e.g. -100) means deposited (invested)
    Positive (e.g. 100) means withdrawn (divested)
    """
    session = db_connection.create_db_session()

    # E.g. "2021-01-01"
    date_of_today: str = datetime.datetime.today().strftime('%Y-%m-%d')

    # get withdrawal if exists
    withdrawal = session.query(Withdrawal). \
        filter(Withdrawal.platform_name == platform_name,
               Withdrawal.date == date_of_today).first()

    # Update withdrawal, if found
    if withdrawal:
        withdrawal.withdrawal = withdrawal_amount
        withdrawal.updated_at = get_time_date_string()
        session.commit()
    # create new withdrawal otherwise
    else:
        withdrawal = Withdrawal()
        withdrawal.platform_name = platform_name
        withdrawal.withdrawal = withdrawal_amount
        withdrawal.date = date_of_today
        withdrawal.created_at = get_time_date_string()

        session.add(withdrawal)
        session.commit()

        withdrawal = session.query(Withdrawal) \
            .filter(Withdrawal.platform_name == platform_name,
                    Withdrawal.date == date_of_today) \
            .first()

    session.close()
    return withdrawal


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


def get_withdrawals_by_platform(platform_name: str) -> dict:
    session = db_connection.create_db_session()
    rows: dict = {}

    # Query specific fields returns list
    query_results: list = session \
        .query(Withdrawal.date, Withdrawal.withdrawal) \
        .filter(Withdrawal.platform_name == platform_name) \
        .all()
    # print(f"{type(filtered_rows)} {filtered_rows=}")

    for row in query_results:
        datetime_object: datetime.datetime = datetime.datetime.strptime(
            row[0], "%Y-%m-%d")
        rows[datetime_object] = row[1]

    # Query all fields (entire table) returns SQLAlchemy object
    # for row in session.query(Withdrawal).filter(
    #         Withdrawal.platform_name == platform_name).all():
    #     datetime_object: datetime.datetime = datetime.datetime.strptime(
    #         row.__dict__["date"], "%Y-%m-%d")
    #     rows[datetime_object] = row.__dict__["withdrawal"]

    session.close()
    return rows


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


def get_total_balance_of_today() -> float:
    session = db_connection.create_db_session()
    date_of_today: str = datetime.datetime.today().strftime(
        '%Y-%m-%d')  # E.g. "2021-01-01"

    total_amount = session.query(Balance.date, func.sum(Balance.balance).label(
        "daily_balance")) \
        .filter(Balance.date == date_of_today) \
        .first()
    session.close()

    if total_amount[1]:  # if not None
        total_amount_rounded: float = round(total_amount.daily_balance, 2)
        print(f"{total_amount.date} TODAY'S TOTAL: {total_amount_rounded}")
        return total_amount_rounded
    else:
        print(f"{date_of_today} TODAY'S TOTAL: 0")
        return 0


def get_last_balance_by_platform(platform_name: str) -> list:
    session = db_connection.create_db_session()

    # last_balance <sqlalchemy.util._collections.result>
    last_balance = session.query(Balance.date, Balance.balance) \
        .filter(Balance.platform_name == platform_name) \
        .group_by(Balance.date) \
        .order_by(Balance.date.desc()) \
        .first()

    session.close()
    return last_balance


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


def get_total_balances_by_day() -> list:
    session = db_connection.create_db_session()

    total_amounts_by_day = session.query(Balance.date,
                                         func.sum(Balance.balance).label(
                                             "daily_balance")) \
        .group_by(Balance.date) \
        .all()

    # for row in total_amounts_by_day:
    #     print(f"{row.date} {round(row.daily_balance, 2)}")

    session.close()
    return total_amounts_by_day


def get_portfolio_size() -> float:
    portfolio_size: float = get_total_balances_by_day()[-1][1]
    return round(portfolio_size, 2)


def get_total_invested() -> float:
    session = db_connection.create_db_session()

    total_invested_result = session.query(
        func.sum(Withdrawal.withdrawal)).first()
    session.close()

    total_invested_float: float = tuple(total_invested_result)[0]
    return round(total_invested_float, 2)


def get_net_profit_loss() -> float:
    return round(get_total_invested() + get_portfolio_size(), 2)


def get_time_date_string() -> str:
    """ Get ISO8601 date and time string ("YYYY-MM-DD HH:MM:SS.SSS")
    Helper function used for for "created_at" and "updated_at" fields
    """
    return str(
        datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds'))
