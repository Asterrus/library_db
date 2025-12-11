from __future__ import annotations

import logging

from litestar.plugins.sqlalchemy import repository

from db.models import AuthorModel

logger = logging.getLogger(__name__)


class AuthorRepository(repository.SQLAlchemyAsyncRepository[AuthorModel]):
    """Author repository."""

    model_type = AuthorModel
