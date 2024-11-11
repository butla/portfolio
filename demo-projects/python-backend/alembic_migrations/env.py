# ruff: noqa: INP001
from logging.config import fileConfig

from alembic import context
import sqlalchemy
import tenacity

from sample_backend.core.config import SETTINGS
from sample_backend.entities import db_models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db_models.Base.metadata


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    sql_engine = sqlalchemy.create_engine(
        SETTINGS.postgres_url,
        poolclass=sqlalchemy.pool.NullPool,
    )

    # When we run migrations during development or testing Postgres from Docker Compose may still be starting.
    _wait_for_postgres(sql_engine)

    with sql_engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


@tenacity.retry(stop=tenacity.stop_after_delay(10), wait=tenacity.wait_fixed(0.2), reraise=True)
def _wait_for_postgres(sql_engine: sqlalchemy.Engine) -> None:
    with sql_engine.connect():
        pass


if context.is_offline_mode():
    raise NotImplementedError("We don't have offline migrations")
else:
    run_migrations_online()
