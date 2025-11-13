# Production образ
FROM python:3.8-slim AS production

WORKDIR /app

ENV APP_ENV=prod
ENV PYTHONPATH=/app/src

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копирование файлов Poetry для установки зависимостей
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-dev --no-root

# Копирование исходного кода
COPY src/ ./src/

# Экспорт порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Development образ
FROM python:3.8-slim AS development

WORKDIR /app

ENV APP_ENV=dev
ENV PYTHONPATH=/app/src

# Установка системных зависимостей включая инструменты разработки
RUN apt-get update && apt-get install -y \
    sqitch \
    libdbd-pg-perl \
    postgresql-client \
    libdbd-sqlite3-perl \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копирование файлов Poetry
COPY pyproject.toml ./

# Установка только зависимостей (без самого проекта)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Копирование всех файлов проекта
COPY . .

# Создание entrypoint для dev среды если есть
RUN if [ -f .ci/files/entrypoint.sh ]; then \
        cp .ci/files/entrypoint.sh /app/entrypoint.sh && \
        chmod +x /app/entrypoint.sh; \
    fi

# Экспорт порта
EXPOSE 8000

# Запуск с горячей перезагрузкой для разработки
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
