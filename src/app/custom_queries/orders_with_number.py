import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def list_orders_with_number(
    session: AsyncSession,
) -> list[dict[str, Any]]:
    logger.debug("list_orders_with_number called")

    stmt = text(
        """
        SELECT
            id,
            reader_id,
            book_id,
            due_date,
            return_date,
            created_at,
            updated_at,
            row_number() over (order by created_at) as order_number
        FROM "order"
        ORDER BY order_number
        """
    )

    result = await session.execute(stmt)
    rows = [dict(row) for row in result.mappings().all()]
    logger.debug("list_orders_with_number fetched %d rows", len(rows))
    return rows
