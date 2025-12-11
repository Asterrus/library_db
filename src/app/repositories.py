from __future__ import annotations

from db.models import AuthorModel, BookModel, OrderModel, ReaderModel
from litestar.plugins.sqlalchemy import repository


class AuthorRepository(repository.SQLAlchemyAsyncRepository[AuthorModel]):
    """Author repository."""

    model_type = AuthorModel


class BookRepository(repository.SQLAlchemyAsyncRepository[BookModel]):
    """Book repository."""

    model_type = BookModel


class ReaderRepository(repository.SQLAlchemyAsyncRepository[ReaderModel]):
    """Reader repository."""

    model_type = ReaderModel


class OrderRepository(repository.SQLAlchemyAsyncRepository[OrderModel]):
    """Order repository."""

    model_type = OrderModel
