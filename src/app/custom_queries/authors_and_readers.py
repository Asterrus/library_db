import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def list_authors_and_readers(
    session: AsyncSession,
    use_union_all: bool = False,
) -> list[dict[str, Any]]:
    logger.debug("list_authors_and_readers called - use_union_all=%s", use_union_all)

    stmt = text(
        f"""
        SELECT first_name, second_name
        FROM author
        {"UNION ALL" if use_union_all else "UNION"}
        SELECT first_name, second_name
        FROM reader
        ORDER BY first_name, second_name
        """
    )

    result = await session.execute(stmt)
    rows = list(result.mappings().all())
    logger.debug("list_authors_and_readers fetched %d rows", len(rows))
    return rows
