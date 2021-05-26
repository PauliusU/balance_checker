import sqlalchemy
from models.model_base import ModelBase


class Balance(ModelBase):
    __tablename__ = 'balances'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    platform_name = sqlalchemy.Column(sqlalchemy.String)
    balance = sqlalchemy.Column(sqlalchemy.Float)
    created_at = sqlalchemy.Column(sqlalchemy.String)
    updated_at = sqlalchemy.Column(sqlalchemy.String)
