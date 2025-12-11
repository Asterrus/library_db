from __future__ import annotations

import logging
from typing import Literal

from litestar import Controller, get
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from custom_queries.authors_and_readers import list_authors_and_readers
from schemas import AuthorsAndReaders

logger = logging.getLogger(__name__)


class CustomQueriesController(Controller):
    tags = ["CustomQueries(Сырые SQL запросы)"]

    @get(path="/authors_and_readers")
    async def list_authors_and_readers(
        self,
        db_session: AsyncSession,
        union_type: Literal["union", "union_all"] = "union",
    ) -> list[AuthorsAndReaders]:
        logger.debug("list_people called - union_type=%s", union_type)

        use_union_all = union_type == "union_all"
        rows = await list_authors_and_readers(db_session, use_union_all=use_union_all)

        type_adapter = TypeAdapter(list[AuthorsAndReaders])
        return type_adapter.validate_python(rows)
