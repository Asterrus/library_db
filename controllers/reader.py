from uuid import UUID

from litestar import Controller, delete, get, post
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import filters
from pydantic import TypeAdapter

from db.models import ReaderModel
from di import provide_readers_repo
from repositories import ReaderRepository
from schemas import Reader, ReaderCreate


class ReaderController(Controller):
    """Reader CRUD"""

    dependencies = {"readers_repo": Provide(provide_readers_repo)}
    tags = ["Readers"]

    @get(path="/readers")
    async def list_readers(
        self,
        readers_repo: ReaderRepository,
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[Reader]:
        results, total = await readers_repo.list_and_count(limit_offset)
        type_adapter = TypeAdapter(list[Reader])
        return OffsetPagination[Reader](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path="/readers")
    async def create_reader(
        self,
        readers_repo: ReaderRepository,
        data: ReaderCreate,
    ) -> Reader:
        obj = await readers_repo.add(
            ReaderModel(**data.model_dump(exclude_unset=True, exclude_none=True)),
        )
        await readers_repo.session.commit()
        return Reader.model_validate(obj)

    @delete(path="/readers/{reader_id:uuid}")
    async def delete_reader(
        self,
        readers_repo: ReaderRepository,
        reader_id: UUID,
    ) -> None:
        _ = await readers_repo.delete(reader_id)
        await readers_repo.session.commit()
