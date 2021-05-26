import os
import sqlalchemy
from models.model_base import ModelBase

dialect: str = "sqlite:///"
db_file_base_name: str = "p2p.sqlite3.db"


def create_db_session() -> sqlalchemy.orm.session.Session:
    # connection - create engine
    engine: sqlalchemy.engine.base.Engine = \
        sqlalchemy.create_engine(
            dialect + get_absolute_db_path(db_file_base_name))

    # create metadata - define and create tables
    ModelBase.metadata.create_all(engine)

    # create session
    session: sqlalchemy.orm.session.sessionmaker = \
        sqlalchemy.orm.sessionmaker(bind=engine)

    return session()


def get_absolute_db_path(base_file) -> str:
    # what folder is this .py file located in
    base_folder: str = os.path.dirname(__file__)

    return os.path.join(base_folder, base_file)
