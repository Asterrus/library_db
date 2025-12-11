import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def books_with_authors_cte(session: AsyncSession) -> list[dict[str, Any]]:
    logger.debug("books_with_authors_cte called")

    stmt = text("""
        WITH author_cte AS (
            SELECT id, first_name, second_name
            FROM author
        ),
        book_cte AS (
            SELECT id, title, author_id, isbn, published_date, description
            FROM book
        )
        SELECT
            b.id,
            b.title,
            b.author_id,
            b.isbn,
            b.published_date,
            b.description,
            a.first_name,
            a.second_name
        FROM book_cte b
        JOIN author_cte a ON a.id = b.author_id
        ORDER BY b.title, a.first_name, a.second_name
    """)

    result = await session.execute(stmt)
    raw = [dict(row) for row in result.mappings().all()]

    rows = [
        {
            "id": r["id"],
            "title": r["title"],
            "isbn": r["isbn"],
            "published_date": r["published_date"],
            "description": r["description"],
            "author": {
                "id": r["author_id"],
                "first_name": r["first_name"],
                "second_name": r["second_name"],
            },
        }
        for r in raw
    ]

    return rows
