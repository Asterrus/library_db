import logging
from collections.abc import Sequence
from typing import TypedDict

from sqlalchemy import Connection
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class ReaderCreate(TypedDict):
    first_name: str
    second_name: str
    phone: str
    email: str


def create_reader(conn: Connection, data: Sequence[ReaderCreate]):
    logger.debug("crud reader create")
    stmt = text("""
    INSERT INTO book(first_name, second_name, phone, email)
    VALUES (:first_name, :second_name, :phone, :email);
    """)
    for line in data:
        conn.execute(stmt, line)
    logger.debug(f"crud reader create. {len(data)} rows inserted")
