import logging
from uuid import UUID

from db.models import BookModel
from di import provide_books_repo
from litestar import Controller, delete, get, post
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import filters
from pydantic import TypeAdapter
from repositories import BookRepository
from schemas import Book, BookCreate, BookWithAuthor
from sqlalchemy.orm import joinedload, selectinload

logger = logging.getLogger(__name__)


class BookController(Controller):
    """Book CRUD"""

    dependencies = {"books_repo": Provide(provide_books_repo)}
    tags = ["Books"]

    @get(path="/books")
    async def list_books(
        self,
        books_repo: BookRepository,
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[BookWithAuthor]:
        logger.debug("list_books called - limit_offset=%s", limit_offset)
        results, total = await books_repo.list_and_count(
            limit_offset,
            load=[joinedload(BookModel.author)],
        )
        type_adapter = TypeAdapter(list[BookWithAuthor])
        return OffsetPagination[BookWithAuthor](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get(path="/books/{book_id:uuid}")
    async def get_book(
        self,
        books_repo: BookRepository,
        book_id: UUID,
    ) -> BookWithAuthor:
        logger.debug("get_book called - book_id=%s", book_id)
        result = await books_repo.get(
            book_id,
            load=[joinedload(BookModel.author)],
        )
        type_adapter = TypeAdapter(BookWithAuthor)
        return type_adapter.validate_python(result)

    @post(path="/books")
    async def create_book(
        self,
        books_repo: BookRepository,
        data: BookCreate,
    ) -> Book:
        logger.debug("create_book called - data=%s", data)
        obj = await books_repo.add(
            BookModel(**data.model_dump(exclude_unset=True, exclude_none=True)),
        )
        await books_repo.session.commit()
        return Book.model_validate(obj)

    @delete(path="/books/{book_id:uuid}")
    async def delete_book(
        self,
        books_repo: BookRepository,
        book_id: UUID,
    ) -> None:
        logger.debug("delete_book called - book_id=%s", book_id)
        _ = await books_repo.delete(book_id)
        await books_repo.session.commit()
