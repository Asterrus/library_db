from __future__ import annotations

import logging

from litestar.plugins.sqlalchemy import repository

from db.models import ReaderModel

logger = logging.getLogger(__name__)


class ReaderRepository(repository.SQLAlchemyAsyncRepository[ReaderModel]):
    """Reader repository."""

    model_type = ReaderModel
