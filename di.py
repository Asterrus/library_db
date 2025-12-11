from sqlalchemy.ext.asyncio import AsyncSession

from repositories import (
    AuthorRepository,
    BookRepository,
    OrderRepository,
    ReaderRepository,
)


async def provide_authors_repo(db_session: AsyncSession) -> AuthorRepository:
    return AuthorRepository(session=db_session)


async def provide_books_repo(db_session: AsyncSession) -> BookRepository:
    return BookRepository(session=db_session)


async def provide_readers_repo(db_session: AsyncSession) -> ReaderRepository:
    return ReaderRepository(session=db_session)


async def orders_readers_repo(db_session: AsyncSession) -> OrderRepository:
    return OrderRepository(session=db_session)
