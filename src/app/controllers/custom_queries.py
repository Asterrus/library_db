from __future__ import annotations

import logging
from typing import Literal

from litestar import Controller, get
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from custom_queries.authors_and_readers import list_authors_and_readers
from custom_queries.cte import books_with_authors_cte
from custom_queries.orders_nulls import list_orders_with_default_return_date
from custom_queries.orders_with_number import list_orders_with_number
from schemas import AuthorsAndReaders, BookWithAuthor, Order, OrderWithNumber

logger = logging.getLogger(__name__)


class CustomQueriesController(Controller):
    tags = ["CustomQueries(Сырые SQL запросы)"]

    @get(
        path="/orders_with_default_return_date",
        description="""
        2. Работа с NULL:
        – Выбор всех заказов с указанием даты возврата или значения по умолчанию
        """,
    )
    async def orders_with_default_return_date(
        self,
        db_session: AsyncSession,
    ) -> list[Order]:
        logger.debug("orders_with_default_return_date called")
        rows = await list_orders_with_default_return_date(db_session)

        type_adapter = TypeAdapter(list[Order])
        return type_adapter.validate_python(rows)

    @get(
        path="/authors_and_readers",
        description="""
        3. Использование UNION vs UNION ALL:
        – Объединение списков читателей и авторов
        """,
    )
    async def list_authors_and_readers(
        self,
        db_session: AsyncSession,
        union_type: Literal["union", "union_all"] = "union",
    ) -> list[AuthorsAndReaders]:
        logger.debug("list_authors_and_readers called - union_type=%s", union_type)

        use_union_all = union_type == "union_all"
        rows = await list_authors_and_readers(db_session, use_union_all=use_union_all)

        type_adapter = TypeAdapter(list[AuthorsAndReaders])
        return type_adapter.validate_python(rows)

    @get(
        path="/books_with_authors",
        description="""
        4. CTE и рекурсивные запросы:
        – Создание иерархического запроса для получения всех книг и их авторов
        """,
    )
    async def books_with_authors(
        self,
        db_session: AsyncSession,
    ) -> list[BookWithAuthor]:
        logger.debug("books_with_authors called")
        rows = await books_with_authors_cte(db_session)

        type_adapter = TypeAdapter(list[BookWithAuthor])
        return type_adapter.validate_python(rows)

    @get(
        path="/orders_with_number",
        description="""
        5. Оконные функции:
        – Использование оконных функций для нумерации заказов:
        """,
    )
    async def orders_with_number(
        self,
        db_session: AsyncSession,
    ) -> list[OrderWithNumber]:
        logger.debug("orders_with_number called")
        rows = await list_orders_with_number(db_session)

        type_adapter = TypeAdapter(list[OrderWithNumber])
        return type_adapter.validate_python(rows)
