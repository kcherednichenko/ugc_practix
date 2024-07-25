from core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dsn = (f'postgresql+psycopg2://{settings.pg_user}:{settings.pg_password}@'
       f'{settings.pg_host}:{settings.pg_port}/{settings.pg_database}')
engine = create_engine(dsn, echo=True, future=True)


def get_session_postgres():
    Session = sessionmaker(bind=engine)
    return Session()
