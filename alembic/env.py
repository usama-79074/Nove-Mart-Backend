from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys
import os

# Project root ko path mein add kar rahe hain taake "app" module import ho sake
sys.path.append(os.getcwd())

from app.core.config import DATABASE_URL
from app.database.database import Base

# Models import
from app.models.user_model import User  # noqa
from app.models.category_model import Category  # noqa
from app.models.product_model import Product  # noqa
from app.models.cart_model import Cart, CartItem  # noqa
from app.models.order_model import Order, OrderItem  # noqa

# Alembic config object
config = context.config

# Database URL set karo
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name:
    try:
        fileConfig(config.config_file_name, disable_existing_loggers=False)
    except Exception:
        pass

# Metadata
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()