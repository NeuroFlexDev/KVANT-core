# Docker Troubleshooting Guide

## Проблема с правами Docker

Если вы видите ошибку:
```
permission denied while trying to connect to the Docker daemon socket
```

### Решение 1: Добавить пользователя в группу docker

```bash
# Добавить текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Перезайти в систему или выполнить
newgrp docker

# Проверить что Docker работает
docker --version
docker ps
```

### Решение 2: Использовать sudo (временно)

```bash
# Запуск с sudo
sudo make dev

# Или напрямую
sudo docker-compose -f docker-compose.dev.yml up --build
```

### Решение 3: Перезапустить Docker daemon

```bash
sudo systemctl restart docker
sudo systemctl enable docker
```

## Исправленные проблемы

### 1. Ошибка Poetry в Dockerfile

**Проблема:** Poetry не может установить проект из-за отсутствия исходного кода.

**Решение:** Используем `--no-root` при установке зависимостей.

### 2. Устаревшая версия Docker Compose

**Проблема:** Warning о устаревшем `version: '3.8'`

**Решение:** Удалили строку version из всех compose файлов.

### 3. Неправильный порт в compose файле

**Проблема:** Синтаксическая ошибка в маппинге портов.

**Решение:** Упростили маппинг портов до фиксированных значений.

## Запуск после исправлений

```bash
# Очистить предыдущие сборки
docker system prune -f

# Запустить в режиме разработки
make dev

# Или напрямую
docker-compose -f docker-compose.dev.yml up --build
```

## Проверка работоспособности

После успешного запуска должны быть доступны:

- **Фронтенд:** http://localhost:5173
- **Бэкенд:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs
- **База данных:** localhost:5432

## Логи для отладки

```bash
# Посмотреть логи всех сервисов
docker-compose -f docker-compose.dev.yml logs

# Логи конкретного сервиса
docker-compose -f docker-compose.dev.yml logs backend
docker-compose -f docker-compose.dev.yml logs frontend
docker-compose -f docker-compose.dev.yml logs postgres
```

## Альтернативный запуск без Docker

Если Docker не работает, можно запустить сервисы напрямую:

### Бэкенд:
```bash
cd omi-dev
pip install poetry
poetry install
poetry shell
export PYTHONPATH=$PWD/src
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Фронтенд:
```bash
cd kvant
npm install
npm run dev
```

### База данных:
Установите PostgreSQL локально или используйте Docker только для базы:
```bash
docker run --name kvant-postgres -e POSTGRES_DB=kvant_dev -e POSTGRES_USER=kvant_user -e POSTGRES_PASSWORD=kvant_password -p 5432:5432 -d postgres:13-alpine
```