import logging
from collections.abc import Sequence
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Connection
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class BookCreate(TypedDict):
    book_title: str
    author_id: int
    isbn: str
    published_date: datetime
    description: str


def create_book(conn: Connection, data: Sequence[BookCreate]):
    logger.debug("crud book create")
    stmt = text("""
    INSERT INTO book(book_title, author_id, isbn, published_date, description)
    VALUES (:book_title, :author_id, :isbn, :published_date, :description);
    """)
    for line in data:
        conn.execute(stmt, line)
    logger.debug(f"crud book create. {len(data)} rows inserted")
