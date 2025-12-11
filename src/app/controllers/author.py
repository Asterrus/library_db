from uuid import UUID

from db.models import AuthorModel
from di import provide_authors_repo
from litestar import Controller, delete, get, post
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import filters
from pydantic import TypeAdapter
from repositories import AuthorRepository
from schemas import Author, AuthorCreate


class AuthorController(Controller):
    """Author CRUD"""

    dependencies = {"authors_repo": Provide(provide_authors_repo)}
    tags = ["Authors"]

    @get(path="/authors")
    async def list_authors(
        self,
        authors_repo: AuthorRepository,
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[Author]:
        results, total = await authors_repo.list_and_count(limit_offset)
        type_adapter = TypeAdapter(list[Author])
        return OffsetPagination[Author](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path="/authors")
    async def create_author(
        self,
        authors_repo: AuthorRepository,
        data: AuthorCreate,
    ) -> Author:
        obj = await authors_repo.add(
            AuthorModel(**data.model_dump(exclude_unset=True, exclude_none=True)),
        )
        await authors_repo.session.commit()
        return Author.model_validate(obj)

    @delete(path="/authors/{author_id:uuid}")
    async def delete_author(
        self,
        authors_repo: AuthorRepository,
        author_id: UUID,
    ) -> None:
        _ = await authors_repo.delete(author_id)
        await authors_repo.session.commit()
