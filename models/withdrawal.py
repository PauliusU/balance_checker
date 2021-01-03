import sqlalchemy
from models.model_base import ModelBase


class Withdrawal(ModelBase):
    __tablename__ = 'withdrawals'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    platform_name = sqlalchemy.Column(sqlalchemy.String)
    withdrawal = sqlalchemy.Column(sqlalchemy.Float)
    created_at = sqlalchemy.Column(sqlalchemy.String)
    updated_at = sqlalchemy.Column(sqlalchemy.String)
