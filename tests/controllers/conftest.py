import pytest
from alembic.command import upgrade
from aiohttp import web
from app.config.app import app_config
from sqlalchemy import create_engine

from app.config.enviroment import load_environment


@pytest.fixture
async def migrated_postgres(alembic_config, postgres):
    upgrade(alembic_config, 'head')
    return postgres



@pytest.fixture
async def api(aiohttp_client, migrated_postgres_connection):
    load_environment()
    app = web.Application()
    app_config(app)
    client = await aiohttp_client(app)

    try:
        yield client, app
    finally:
        await client.close()


@pytest.fixture
def migrated_postgres_connection(migrated_postgres):
    engine = create_engine(migrated_postgres)
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
        engine.dispose()