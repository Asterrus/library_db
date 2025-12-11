from __future__ import annotations

import datetime
from typing import Optional
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
    description: Optional[str] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime


class BookCreate(BaseModel):
    title: str
    author_id: UUID
    isbn: str
    published_date: datetime.date
    description: Optional[str] = None


class Reader(BaseModel):
    id: UUID | None
    first_name: str
    second_name: str
    phone: str
    email: Optional[str] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime


class ReaderCreate(BaseModel):
    first_name: str
    second_name: str
    phone: str
    email: Optional[str] = None


class ReaderUpdate(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class Order(BaseModel):
    id: UUID | None
    reader_id: UUID
    book_id: UUID
    due_date: datetime.date
    return_date: datetime.date

    created_at: datetime.datetime
    updated_at: datetime.datetime


class OrderCreate(BaseModel):
    reader_id: UUID
    book_id: UUID
    due_date: datetime.date
