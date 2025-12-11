from __future__ import annotations

import datetime
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase, UUIDBase
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AuthorModel(UUIDBase):
    __tablename__ = "author"
    first_name: Mapped[str] = mapped_column(String(200))
    second_name: Mapped[str] = mapped_column(String(200))
    books: Mapped[list[BookModel]] = relationship(
        back_populates="author",
        lazy="noload",
    )


class BookModel(UUIDAuditBase):
    __tablename__ = "book"
    title: Mapped[str] = mapped_column(String())
    author_id: Mapped[UUID] = mapped_column(ForeignKey("author.id"))
    isbn: Mapped[str] = mapped_column(String(13))
    published_date: Mapped[datetime.date] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(String(), nullable=True)
    author: Mapped[AuthorModel] = relationship(
        back_populates="books",
        lazy="joined",
        innerjoin=True,
    )

    orders: Mapped[list[OrderModel]] = relationship(
        back_populates="book",
        lazy="noload",
    )


class ReaderModel(UUIDAuditBase):
    __tablename__ = "reader"
    first_name: Mapped[str] = mapped_column(String(200))
    second_name: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str | None] = mapped_column(String(15))
    email: Mapped[str | None] = mapped_column(String(200))

    orders: Mapped[list[OrderModel]] = relationship(
        back_populates="reader",
        lazy="noload",
    )


class OrderModel(UUIDAuditBase):
    __tablename__ = "order"
    reader_id: Mapped[UUID] = mapped_column(ForeignKey("reader.id"))
    book_id: Mapped[UUID] = mapped_column(ForeignKey("book.id"))
    due_date: Mapped[datetime.date] = mapped_column(Date)
    return_date: Mapped[datetime.date | None] = mapped_column(Date)

    reader: Mapped[ReaderModel] = relationship(
        back_populates="orders",
        lazy="joined",
        innerjoin=True,
    )
    book: Mapped[BookModel] = relationship(
        back_populates="orders",
        lazy="joined",
        innerjoin=True,
    )
