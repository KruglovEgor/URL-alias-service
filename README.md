# URL Alias Service

Сервис для создания коротких URL с возможностью отслеживания статистики переходов.

## Возможности

- Создание коротких URL из длинных
- Автоматическое устаревание ссылок
- Статистика переходов
- API с аутентификацией
- Swagger документация

## Требования

- Python 3.10+
- PostgreSQL
- Poetry (для управления зависимостями)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/url-alias-service.git
cd url-alias-service
```

2. Установите зависимости с помощью Poetry:
```bash
poetry install
```

3. Создайте файл .env в корневой директории:
```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=url_alias
SECRET_KEY=your-secret-key-here
```

4. Примените миграции базы данных:
```bash
poetry run alembic upgrade head
```

## Запуск

1. Запустите сервер разработки:
```bash
poetry run uvicorn app.main:app --reload
```

2. Откройте Swagger документацию:
```
http://localhost:8000/docs
```

## API Endpoints

### Публичные эндпоинты

- `GET /{short_code}` - Перенаправление на оригинальный URL

### Приватные эндпоинты (требуют аутентификации)

- `POST /api/v1/urls` - Создание короткого URL
- `GET /api/v1/urls` - Получение списка URL
- `DELETE /api/v1/urls/{url_id}` - Деактивация URL
- `GET /api/v1/urls/stats` - Получение статистики переходов

## Разработка

### Запуск тестов

```bash
poetry run pytest
```

### Форматирование кода

```bash
poetry run black .
poetry run isort .
```

### Проверка типов

```bash
poetry run mypy .
```

## Лицензия

MIT 