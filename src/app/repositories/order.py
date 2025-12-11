from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import OrderModel

logger = logging.getLogger(__name__)


class OrderRepository:
    """Order repository implemented with raw SQL."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_and_count(self, limit_offset: Any) -> tuple[list[dict[str, Any]], int]:
        logger.debug("OrderRepository list_and_count")

        stmt = text("""
            SELECT
                id,
                reader_id,
                book_id,
                due_date,
                return_date,
                created_at,
                updated_at
            FROM "order"
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :offset
        """)
        result = await self.session.execute(
            stmt,
            {"limit": limit_offset.limit, "offset": limit_offset.offset},
        )
        items = list(result.mappings().all())

        total_result = await self.session.execute(
            text('''SELECT COUNT(*) AS total FROM "order"'''),
        )
        total = int(total_result.scalar_one())
        return items, total

    async def add(self, model: OrderModel) -> dict[str, Any]:
        logger.debug("OrderRepository add")

        stmt = text("""
            INSERT INTO "order" (reader_id, book_id, due_date)
            VALUES (:reader_id, :book_id, :due_date)
            RETURNING id, reader_id, book_id, due_date, return_date, created_at, updated_at
        """)

        params = {
            "reader_id": model.reader_id,
            "book_id": model.book_id,
            "due_date": model.due_date,
        }
        result = await self.session.execute(stmt, params)
        row = result.mappings().one()
        return dict(row)

    async def delete(self, order_id: UUID) -> None:
        logger.debug("OrderRepository delete")

        await self.session.execute(
            text('DELETE FROM "order" WHERE id = :id'),
            {"id": order_id},
        )
