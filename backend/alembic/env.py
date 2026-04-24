from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

from app.core.settings import settings
from app.db.base import Base

from app.models.part import Part
from app.models.history import PartHistory

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online():
    engine = create_engine(settings.DATABASE_URL)

    with engine.begin() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        context.run_migrations()


if context.is_offline_mode():
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations_online()