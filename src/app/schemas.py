from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    model_config = {"from_attributes": True}


class Author(BaseModel):
    id: UUID | None
    first_name: str
    second_name: str


class AuthorCreate(BaseModel):
    first_name: str
    second_name: str


class Book(BaseModel):
    id: UUID | None
    title: str
    author_id: UUID
    isbn: str
    published_date: datetime.date
    description: str | None = None

    created_at: datetime.datetime
    updated_at: datetime.datetime


class BookCreate(BaseModel):
    title: str
    author_id: UUID
    isbn: str
    published_date: datetime.date
    description: str | None = None


class BookWithAuthor(BaseModel):
    id: UUID
    title: str
    isbn: str
    published_date: datetime.date
    description: str | None = None
    author: Author


class Reader(BaseModel):
    id: UUID | None
    first_name: str
    second_name: str
    phone: str
    email: str | None = None


class AuthorsAndReaders(BaseModel):
    first_name: str
    second_name: str


class ReaderCreate(BaseModel):
    first_name: str
    second_name: str
    phone: str
    email: str | None = None


class ReaderUpdate(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    phone: str | None = None
    email: str | None = None


class Order(BaseModel):
    id: UUID | None
    reader_id: UUID
    book_id: UUID
    due_date: datetime.date
    return_date: datetime.date | None = None

    created_at: datetime.datetime
    updated_at: datetime.datetime


class OrderCreate(BaseModel):
    reader_id: UUID
    book_id: UUID
    due_date: datetime.date
