import logging
from collections.abc import Sequence
from typing import TypedDict

from sqlalchemy import Connection
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class AuthorCreate(TypedDict):
    first_name: str
    second_name: str


def create_author(conn: Connection, data: Sequence[AuthorCreate]):
    logger.debug("crud author create")
    stmt = text("""
    INSERT INTO author(first_name, second_name)
    VALUES (:first_name,:second_name);
    """)
    for line in data:
        conn.execute(stmt, line)
    logger.debug(f"crud author create. {len(data)} rows inserted")
