from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import dotenv_values
from pathlib import Path

from src.models import Base

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / '.env'


def get_engine(driver, user, passwd, host, port, db):
    url = f'{driver}://{user}:{passwd}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)

    engine = create_engine(
        url, pool_size=50, isolation_level="SERIALIZABLE", echo=True)
    return engine


def get_engine_from_env():
    config = dotenv_values(CONFIG_PATH)
    keys = ['DRIVER', 'USER', 'PASSWD', 'HOST', 'PORT', 'DB']

    if not all([key in keys for key in config.keys()]):
        raise Exception('Bad config file')

    return get_engine(config['DRIVER'],
                      config['USER'],
                      config['PASSWD'],
                      config['HOST'],
                      config['PORT'],
                      config['DB'])


def get_session(engine) -> sessionmaker:
    return sessionmaker(bind=engine)


def init_db(engine) -> None:
    Base.metadata.create_all(bind=engine)
