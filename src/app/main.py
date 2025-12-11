from __future__ import annotations

import logging

from controllers.author import AuthorController
from controllers.book import BookController
from controllers.order import OrderController
from controllers.reader import ReaderController
from db.engine import get_database_url
from litestar import Litestar
from litestar.di import Provide
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from pagination import provide_limit_offset_pagination

session_config = AsyncSessionConfig(expire_on_commit=False)


sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=get_database_url(),
    session_config=session_config,
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def on_startup() -> None:
    """Initializes the database."""
    print("on_startup")
    async with sqlalchemy_config.get_engine().begin() as conn:
        from sqlalchemy import text

        print(f"{conn =}")
        await conn.execute(text("select 1"))
        await conn.execute(text("select * from author;"))
        print("ok")
    # async with sqlalchemy_config.get_engine().begin() as conn:
    #     await conn.run_sync(base.UUIDBase.metadata.create_all)


app = Litestar(
    route_handlers=[
        AuthorController,
        BookController,
        ReaderController,
        OrderController,
    ],
    on_startup=[on_startup],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    dependencies={"limit_offset": Provide(provide_limit_offset_pagination)},
    debug=True,
)
