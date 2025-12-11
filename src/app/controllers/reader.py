import logging
from uuid import UUID

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import filters
from pydantic import TypeAdapter

from db.models import ReaderModel
from di import provide_readers_repo
from repositories import ReaderRepository
from schemas import Reader, ReaderCreate, ReaderUpdate

logger = logging.getLogger(__name__)


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
        logger.debug("list_readers called - limit_offset=%s", limit_offset)
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
        logger.debug("create_reader called - data=%s", data)
        obj = await readers_repo.add(
            ReaderModel(**data.model_dump(exclude_unset=True, exclude_none=True)),
        )
        await readers_repo.session.commit()
        return Reader.model_validate(obj)

    @put(path="/readers/{reader_id:uuid}")
    async def update_reader(
        self,
        readers_repo: ReaderRepository,
        reader_id: UUID,
        data: ReaderUpdate,
    ) -> Reader:
        obj = await readers_repo.session.get(ReaderModel, reader_id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Reader not found")

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(obj, field, value)

        updated = await readers_repo.update(obj, auto_commit=True)

        return Reader.model_validate(updated, from_attributes=True)

    @delete(path="/readers/{reader_id:uuid}")
    async def delete_reader(
        self,
        readers_repo: ReaderRepository,
        reader_id: UUID,
    ) -> None:
        logger.debug("delete_reader called - reader_id=%s", reader_id)
        _ = await readers_repo.delete(reader_id)
        await readers_repo.session.commit()
