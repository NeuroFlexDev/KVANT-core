# Синхронизация бэкенда и фронтенда

## Обзор

Полностью переработана схема работы с опросниками: бэкенд FastAPI теперь хранит формы в новой структуре базы данных, а фронтенд React использует контекст для сохранения/восстановления состояний шагов. Добавлены CRUD‑эндпоинты для личных форм и переработан UI личного кабинета.

## Новые возможности

### Бэкенд (`omi-dev/src`)

- Добавлена схема `app.questionnaire_form` и `app.questionnaire_form_section` (см. миграцию `migrations/deploy/002_questionnaire_forms.sql`).
- Новый слой доступа `dblayer/questionnaire.py` и SQL‑набор `dblayer/sql/questionnaire/forms.sql`.
- Handler `handlers/questionnaire.py` реализует бизнес-логику создания/обновления/удаления форм и секций.
- API `api/questionnaire.py` предоставляет REST:
  - `GET /api/questionnaire/forms` — список форм текущего пользователя.
  - `POST /api/questionnaire/forms` — создание формы (при желании с секциями-шаблонами).
  - `GET /api/questionnaire/forms/{form_id}` — детальная форма с секциями.
  - `PATCH /api/questionnaire/forms/{form_id}` — обновление метаданных (например, текущего шага/статуса).
  - `DELETE /api/questionnaire/forms/{form_id}` — мягкое удаление.
  - `PUT /api/questionnaire/forms/{form_id}/sections/{section_key}` — upsert данных шага.
- Значения подключения к БД теперь по умолчанию указывают на локальный PostgreSQL (`settings.py`).

### Фронтенд (`kvant/src`)

- Добавлены API-обёртки `api/questionnaire.ts` и `api/auth.ts`.
- `AuthContext` хранит access/refresh-токены, перехватывает 401 и автоматически обновляет access токен.
- Появилась страница `/login` с формой аутентификации; все остальные маршруты защищены `RequireAuth`.
- Главная (`/`) — список опросников (`Dashboard`), отображает пользователя и позволяет выйти из системы.
- Страница `/forms/:id` оборачивается в `FormProvider`, а шаги (`GeneralProvisions`, `MainArchitecture`, `SummaryInfo`, `EngineeringSolution`, `CompositionSection`) работают с контекстом вместо локальных axios-запросов.
- Добавлены default‑состояния и автосохранение шагов, кнопки «Сохранить»/«Рассчитать» фиксируют только изменившиеся данные.

## Локальная база данных

- По умолчанию `settings.py` указывает на локальный PostgreSQL (`localhost:5432`, БД `kvant_dev`).
- Добавлен скрипт `database/sync_prod_to_local.sh`, который выгружает прод в дамп и разворачивает его локально (см. `database/README.md`).
- После восстановления прод-дампа обязательно прогоните миграции (`sqitch deploy`).

## Как применить миграции БД

```bash
cd omi-dev/src
sqitch deploy   # или psql -f migrations/deploy/002_questionnaire_forms.sql
```

## Запуск для разработки

```bash
# Backend
cd omi-dev
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd kvant
npm install
npm run dev
```

Для контроля на стороне фронтенда выполните `npm run build` — конфигурация скорректирована под новый API.

API документация доступна по адресу: `http://localhost:8000/api/docs`

## Следующие шаги

- Настроить unit-тесты на ключевые сценарии опросника и аутентификации.
- Подключить валидацию входных данных на стороне API (Pydantic-схемы с дополнительными проверками).
- Добавить UI для регистрации/восстановления пароля (при необходимости).

## Примечания

- CORS настроен для разработки (3000/5173), production не трогаем.
- Авторизация работает на access/refresh токенах (`X-Auth-Token`); refresh хранится только локально и не уходит в запросы.
- Для работы фронтенда обязательно загрузите локальную копию продовых данных или создайте тестового пользователя вручную.
