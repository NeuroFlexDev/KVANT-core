-- Инициализация базы данных для Kvant Core
-- Этот скрипт выполняется при первом запуске PostgreSQL контейнера

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Создание схем (если требуется)
-- CREATE SCHEMA IF NOT EXISTS kvant;

-- Базовые таблицы будут созданы через миграции FastAPI/SQLAlchemy
-- Здесь можно добавить начальные данные, если необходимо

-- Пример: создание начальных данных
-- INSERT INTO users (email, is_active) VALUES ('admin@kvant.id', true) ON CONFLICT DO NOTHING;

-- Логирование
\echo 'Database initialization completed successfully'