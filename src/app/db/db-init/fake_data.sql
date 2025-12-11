SET LOCAL synchronous_commit TO OFF;
SET LOCAL session_replication_role = replica;

BEGIN;
CREATE UNLOGGED TABLE tmp_author AS
SELECT 'Name_' || g AS first_name, 'Surname_' || g AS second_name
FROM generate_series(1,50000) g;

INSERT INTO author (first_name, second_name)
SELECT first_name, second_name FROM tmp_author;

CREATE UNLOGGED TABLE tmp_book AS
SELECT
  'Book_' || g AS book_title,
  (floor(random() * 50000) + 1)::bigint AS author_id,
  lpad(g::text, 13, '0') AS isbn,
  (date '1900-01-01' + (random() * 365*120)::int) AS published_date,
  'Description: ' || g AS description
FROM generate_series(1,1000000) g;

INSERT INTO book (book_title, author_id, isbn, published_date, description)
SELECT book_title, author_id, isbn, published_date, description FROM tmp_book;

CREATE UNLOGGED TABLE tmp_reader AS
SELECT
  'Name_' || g AS first_name,
  'Surname_' || g AS second_name,
  'phone_' || g AS phone,
  'email_' || g AS email
FROM generate_series(1,10000) g;

INSERT INTO reader(first_name, second_name, phone, email)
SELECT first_name, second_name, phone, email FROM tmp_reader;

CREATE UNLOGGED TABLE tmp_order AS
SELECT
  (floor(random() * 10000) + 1)::bigint AS reader_id,
  (floor(random() * 1000000) + 1)::bigint AS book_id,
  now() - (random() * interval '365 days') AS order_date,
  now() + (random() * interval '30 days') AS due_date
FROM generate_series(1,100000) g;

INSERT INTO "order" (reader_id, book_id, order_date, due_date)
SELECT reader_id, book_id, order_date, due_date FROM tmp_order;

COMMIT;
