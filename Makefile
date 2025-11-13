.PHONY: help dev prod build down logs clean

# Цвета для вывода
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color

help: ## Показать справку
	@echo "$(GREEN)Доступные команды:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

dev: ## Запустить в режиме разработки
	@echo "$(GREEN)Запуск в режиме разработки...$(NC)"
	@cp .env.dev .env
	docker-compose -f docker-compose.dev.yml up --build

dev-sudo: ## Запустить в режиме разработки с sudo
	@echo "$(GREEN)Запуск в режиме разработки с sudo...$(NC)"
	@cp .env.dev .env
	sudo docker-compose -f docker-compose.dev.yml up --build

dev-internal: ## Запустить без внешнего порта БД (избегает конфликтов)
	@echo "$(GREEN)Запуск в режиме разработки (БД только внутри)...$(NC)"
	@cp .env.dev .env
	docker-compose -f docker-compose.dev-internal.yml up --build

dev-internal-sudo: ## Запустить без внешнего порта БД с sudo
	@echo "$(GREEN)Запуск в режиме разработки (БД только внутри) с sudo...$(NC)"
	@cp .env.dev .env
	sudo docker-compose -f docker-compose.dev-internal.yml up --build

dev-detached: ## Запустить в режиме разработки в фоне
	@echo "$(GREEN)Запуск в режиме разработки в фоне...$(NC)"
	@cp .env.dev .env
	docker-compose -f docker-compose.dev.yml up --build -d

prod: ## Запустить в режиме продакшена
	@echo "$(GREEN)Запуск в режиме продакшена...$(NC)"
	@if [ ! -f .env.prod ]; then echo "$(RED)Ошибка: .env.prod не найден!$(NC)"; exit 1; fi
	@cp .env.prod .env
	docker-compose -f docker-compose.prod.yml up --build -d

build: ## Собрать все образы
	@echo "$(GREEN)Сборка всех образов...$(NC)"
	docker-compose build

build-dev: ## Собрать образы для разработки
	@echo "$(GREEN)Сборка образов для разработки...$(NC)"
	docker-compose -f docker-compose.dev.yml build

build-prod: ## Собрать образы для продакшена
	@echo "$(GREEN)Сборка образов для продакшена...$(NC)"
	docker-compose -f docker-compose.prod.yml build

down: ## Остановить все контейнеры
	@echo "$(YELLOW)Остановка всех контейнеров...$(NC)"
	docker-compose down
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.prod.yml down

down-v: ## Остановить контейнеры и удалить volumes
	@echo "$(RED)Остановка контейнеров и удаление volumes...$(NC)"
	docker-compose down -v
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose -f docker-compose.prod.yml down -v

logs: ## Показать логи всех сервисов
	docker-compose logs -f

logs-backend: ## Показать логи бэкенда
	docker-compose logs -f backend

logs-frontend: ## Показать логи фронтенда
	docker-compose logs -f frontend

logs-db: ## Показать логи базы данных
	docker-compose logs -f postgres

restart: ## Перезапустить все сервисы
	@echo "$(YELLOW)Перезапуск сервисов...$(NC)"
	docker-compose restart

restart-backend: ## Перезапустить только бэкенд
	docker-compose restart backend

restart-frontend: ## Перезапустить только фронтенд
	docker-compose restart frontend

shell-backend: ## Войти в контейнер бэкенда
	docker-compose exec backend bash

shell-frontend: ## Войти в контейнер фронтенда
	docker-compose exec frontend sh

shell-db: ## Войти в базу данных
	docker-compose exec postgres psql -U kvant_user -d kvant_dev

clean: ## Очистить неиспользуемые образы и контейнеры
	@echo "$(RED)Очистка неиспользуемых Docker ресурсов...$(NC)"
	docker system prune -f
	docker image prune -f
	docker volume prune -f

clean-all: ## Полная очистка (ОПАСНО!)
	@echo "$(RED)ВНИМАНИЕ: Это удалит ВСЕ Docker ресурсы!$(NC)"
	@read -p "Вы уверены? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "\n$(RED)Удаление всех Docker ресурсов...$(NC)"; \
		docker system prune -a -f --volumes; \
	else \
		echo "\n$(GREEN)Отменено.$(NC)"; \
	fi

setup: ## Первоначальная настройка
	@echo "$(GREEN)Первоначальная настройка...$(NC)"
	@if [ ! -f .env ]; then cp .env.dev .env; echo "$(GREEN)Создан .env файл из .env.dev$(NC)"; fi
	@echo "$(GREEN)Готово! Теперь можно запустить: make dev$(NC)"

docker-setup: ## Настроить права Docker
	@echo "$(GREEN)Настройка прав Docker...$(NC)"
	sudo usermod -aG docker $$USER
	@echo "$(YELLOW)Перезайдите в систему или выполните: newgrp docker$(NC)"
	@echo "$(YELLOW)Затем запустите: make dev$(NC)"

ps: ## Показать статус контейнеров
	docker-compose ps

top: ## Показать процессы в контейнерах
	docker-compose top

# Команды для тестирования
test-backend: ## Запустить тесты бэкенда
	docker-compose exec backend python -m pytest

test-frontend: ## Запустить тесты фронтенда
	docker-compose exec frontend npm test

# Команды для работы с базой данных
db-migrate: ## Выполнить миграции базы данных
	docker-compose exec backend python -m alembic upgrade head

db-backup: ## Создать бэкап базы данных
	@mkdir -p ./backups
	docker-compose exec postgres pg_dump -U kvant_user kvant_dev > ./backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Бэкап создан в ./backups/$(NC)"

db-restore: ## Восстановить базу данных из бэкапа (используйте: make db-restore FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then echo "$(RED)Укажите файл: make db-restore FILE=backup.sql$(NC)"; exit 1; fi
	docker-compose exec -T postgres psql -U kvant_user kvant_dev < ./backups/$(FILE)
	@echo "$(GREEN)База данных восстановлена из $(FILE)$(NC)"