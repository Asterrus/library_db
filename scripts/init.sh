#!/bin/bash
set -e

echo "Создаём таблицы"
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-scripts/init_scheme.sql
echo "Таблицы созданы"

echo "Заполняем таблицы сгенерированными данными"
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-scripts/fake_data.sql
echo "Таблицы заполненны"
