# Локальное копирование базы данных

> **Важно:** Скрипты ниже работают только с вашей локальной средой. Они используют `pg_dump`/`pg_restore` для получения дампа с продакшена и загрузки его в локальную БД. Продовая база при этом не модифицируется.

## Предварительные требования

1. Установленный PostgreSQL клиент (`pg_dump`, `pg_restore`, `psql`).
2. Доступ к продовой БД (хост, порт, пользователь, пароль). Пароль передаётся только через переменные окружения.
3. Локальная PostgreSQL, например та, что поднимается через `docker-compose.dev.yml`.

## Шаги

1. Поднимите локальный Postgres (если ещё не запущен):
   ```bash
   docker compose -f docker-compose.dev.yml up -d postgres
   ```

2. Экспортируйте необходимые переменные окружения:
   ```bash
   export PROD_DB_HOST=prod-hostname
   export PROD_DB_PORT=6432
   export PROD_DB_NAME=omi_dev
   export PROD_DB_USER=omi-admin993
   export PROD_DB_PASSWORD='****************'
   export PROD_DB_SSLMODE=require               # если прод требует SSL
   export PROD_DB_SSLROOTCERT=/path/to/root.crt # файл корневого сертификата

   export LOCAL_DB_HOST=localhost
   export LOCAL_DB_PORT=5432
   export LOCAL_DB_NAME=kvant_dev
   export LOCAL_DB_USER=kvant_user
   export LOCAL_DB_PASSWORD=kvant_password
   # при необходимости можно задать LOCAL_DB_SSLMODE/LOCAL_DB_SSLROOTCERT
   # RESTORE_FILTER_REGEX позволяет вырезать несовместимые конструкции из дампа (по умолчанию удаляется SET transaction_timeout)
```

3. Запустите скрипт:
   ```bash
   chmod +x database/sync_prod_to_local.sh
   ./database/sync_prod_to_local.sh
   ```

Скрипт сохранит дамп во временный `/tmp/kvant_prod.dump`, пересоздаст локальную базу `kvant_dev`, восстановит дамп и удалит временный файл.

4. После восстановления выполните миграции backend-а:
   ```bash
   cd omi-dev/src
   sqitch deploy  # или psql -f migrations/deploy/002_questionnaire_forms.sql
   ```

Теперь backend может работать с локальной копией продовых данных, не затрагивая production.
