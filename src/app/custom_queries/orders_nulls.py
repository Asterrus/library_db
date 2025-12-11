import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def list_orders_with_default_return_date(
    session: AsyncSession,
) -> list[dict[str, Any]]:
    logger.debug("list_orders_with_default_return_date called")

    stmt = text(
        """
        SELECT
            id,
            reader_id,
            book_id,
            due_date,
            COALESCE(return_date, CURRENT_DATE) AS return_date,
            created_at,
            updated_at
        FROM "order"
        ORDER BY created_at
        """
    )

    result = await session.execute(stmt)
    rows = [dict(row) for row in result.mappings().all()]
    logger.debug("list_orders_with_default_return_date fetched %d rows", len(rows))
    return rows
