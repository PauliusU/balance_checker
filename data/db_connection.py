import sqlalchemy
from models.model_base import ModelBase

dialect = "sqlite:///"
db_file_path: str = "database.sqlite"


def create_db_session() -> sqlalchemy.orm.session.Session:
    # connection - create engine
    engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(dialect + db_file_path)

    # create metadata - define and create tables
    ModelBase.metadata.create_all(engine)

    # create session
    session: sqlalchemy.orm.session.sessionmaker = sqlalchemy.orm.sessionmaker(bind=engine)

    return session()
