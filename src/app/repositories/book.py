from __future__ import annotations

import logging

from litestar.plugins.sqlalchemy import repository

from db.models import BookModel

logger = logging.getLogger(__name__)


class BookRepository(repository.SQLAlchemyAsyncRepository[BookModel]):
    """Book repository."""

    model_type = BookModel
