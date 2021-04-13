 
import os
import uuid
from types import SimpleNamespace
import pytest
from sqlalchemy_utils import create_database, drop_database
from app.config.enviroment import load_environment
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from app.config.db import get_database_url, make_alembic_config


def get_revisions():
    options = SimpleNamespace(config='alembic.ini', pg_url=None,
                              name='alembic', raiseerr=False, x=None)
    config = make_alembic_config(options)

    revisions_dir = ScriptDirectory.from_config(config)

    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions

@pytest.fixture
def postgres():
    load_environment()
    tmp_name = '.'.join([uuid.uuid4().hex, 'pytest'])
    url = get_database_url() + tmp_name
    print(url)
    create_database(url)
    
    try:
        yield url
    finally:
        drop_database(url)


@pytest.fixture()
def alembic_config(postgres):
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
                                  pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)