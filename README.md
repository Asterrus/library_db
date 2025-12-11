### Описание

База данных для библиотеки. PostgreSQL. Веб фреймворк - Litestar.

Для таблицы Заказов CRUD операции через сырые SQL запросы, для остальных таблиц через ORM.
SQL запросы для заказов: src/app/repositories/order.py
SQL запросы для Части 3: src/app/custom_queries

Не нашел куда прикрутить рекурсивный запрос, не стал делать.

### Инструменты

- docker
- docker-compose
- uv

### Запуск

1. Клонировать репозиторий и перейти в директорию проекта:

   ```bash
   git clone ...
   cd library_db
   ```

2. Создать .env файл с переменными окружения:

   ```bash
   cp .env.example .env
   ```

3. Запустить docker-compose для запуска базы данных, создания таблиц и запуска веб-сервера:

   ```bash
   docker compose up -d
   ```

4. Открыть документацию:

   ```bash
   http://localhost:8005/schema/swagger
   ```
