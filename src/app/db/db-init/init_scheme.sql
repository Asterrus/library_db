CREATE TABLE author (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name varchar(200) not null,
  second_name varchar(200) not null
);

CREATE TABLE book (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title text not null,
  author_id uuid not null references author (id),
  isbn varchar(13) not null,
  published_date date not null,
  description text,
  created_at timestamp not null default now(),
  updated_at timestamp not null default now()
);

CREATE TABLE reader (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name varchar(200) not null,
  second_name varchar(200) not null,
  phone varchar(15),
  email varchar(200),
  created_at timestamp not null default now(),
  updated_at timestamp not null default now()
);

CREATE TABLE "order" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reader_id uuid not null references reader (id),
  book_id uuid not null references book (id),
  due_date date not null,
  return_date date,
  created_at timestamp not null default now(),
  updated_at timestamp not null default now()
);
