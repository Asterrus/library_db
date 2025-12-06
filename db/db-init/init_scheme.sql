CREATE TABLE author (
  author_id bigint generated always as identity primary key,
  first_name varchar(200) not null,
  second_name varchar(200) not null
);

CREATE TABLE book (
  book_id bigint generated always as identity primary key,
  book_title varchar(200) not null,
  author_id bigint not null references Author (author_id),
  isbn varchar(13) not null,
  published_date date,
  description text
);

CREATE TABLE reader (
  reader_id bigint generated always as identity primary key,
  first_name varchar(200) not null,
  second_name varchar(200) not null,
  phone varchar(15),
  email varchar(200)
);

CREATE TABLE "order" (
  order_id bigint generated always as identity primary key,
  reader_id bigint not null references Reader (reader_id),
  book_id bigint not null references Book (book_id),
  order_date timestamp not null default now(),
  due_date timestamp not null,
  return_date timestamp
);
