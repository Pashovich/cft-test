import config
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from pathlib import Path
from alembic.config import Config
PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()

def get_database_url():
    DATABASE_USER = os.getenv("DATABASE_USER",'postgres')
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD",'123')
    DATABASE_HOST = os.getenv('DATABASE_HOST','localhost')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'test')

    return f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'


def get_session():
    engine = get_engine()
    return Session(engine)

def get_engine():

    engine = create_engine(
        get_database_url(),
        pool_pre_ping=True
    )
    return engine

def make_alembic_config(cmd_opts,
                        base_path = PROJECT_PATH):
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name,
                    cmd_opts=cmd_opts)

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))
    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config