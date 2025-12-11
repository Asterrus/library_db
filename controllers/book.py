from uuid import UUID

from litestar import Controller, delete, get, post
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import filters
from pydantic import TypeAdapter

from db.models import BookModel
from di import provide_books_repo
from repositories import BookRepository
from schemas import Book, BookCreate


class BookController(Controller):
    """Book CRUD"""

    dependencies = {"books_repo": Provide(provide_books_repo)}
    tags = ["Books"]

    @get(path="/books")
    async def list_books(
        self,
        books_repo: BookRepository,
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[Book]:
        results, total = await books_repo.list_and_count(limit_offset)
        type_adapter = TypeAdapter(list[Book])
        return OffsetPagination[Book](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path="/books")
    async def create_book(
        self,
        books_repo: BookRepository,
        data: BookCreate,
    ) -> Book:
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
        _ = await books_repo.delete(book_id)
        await books_repo.session.commit()
