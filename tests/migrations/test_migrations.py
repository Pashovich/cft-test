from types import SimpleNamespace

import pytest
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


@pytest.mark.parametrize('revision', get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)