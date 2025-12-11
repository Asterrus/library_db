import logging
from collections.abc import Sequence
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Connection
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class OrderCreate(TypedDict):
    reader_id: int
    book_id: int
    order_date: datetime
    due_date: datetime
    return_date: datetime


def create_order(conn: Connection, data: Sequence[OrderCreate]):
    logger.debug("crud order create")
    stmt = text("""
    INSERT INTO book(reader_id, book_id, order_date, due_date, return_date)
    VALUES (:reader_id, :book_id, :order_date, :due_date, :return_date);
    """)
    for line in data:
        conn.execute(stmt, line)
    logger.debug(f"crud order create. {len(data)} rows inserted")
