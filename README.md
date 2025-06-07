# URL Alias Service

Сервис для создания коротких алиасов для длинных URL-адресов.

## Технологии

- FastAPI
- PostgreSQL
- Docker
- SQLAlchemy
- Pydantic

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/url-alias-service.git
cd url-alias-service
```

2. Запустите с помощью Docker Compose:
```bash
docker-compose up -d
```

Сервис будет доступен по адресу: http://localhost:8000

## API Endpoints

### Swagger UI

Для удобного тестирования API доступен Swagger UI по адресу: http://localhost:8000/docs

В Swagger UI вы можете:
1. Просмотреть все доступные эндпоинты
2. Протестировать каждый эндпоинт через интерактивный интерфейс
3. Увидеть схемы запросов и ответов
4. Просмотреть модели данных
5. Выполнить запросы с разными параметрами

### Доступные эндпоинты

1. `GET /` - Проверка работоспособности сервиса
2. `GET /health` - Проверка состояния сервиса
3. `POST /urls/` - Создание короткого URL
4. `GET /urls/{alias}` - Получение информации о URL по алиасу
5. `GET /{alias}` - Редирект на оригинальный URL

## Разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл .env с настройками:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/url_alias
SECRET_KEY=your-secret-key
```

3. Запустите сервис:
```bash
uvicorn app.main:app --reload
```

## Тестирование

### Тестирование через Swagger UI

1. Откройте http://localhost:8000/docs в браузере
2. Для создания короткого URL:
   - Найдите эндпоинт POST /urls/
   - Нажмите "Try it out"
   - Введите URL в формате:
   ```json
   {
     "original_url": "https://example.com/very/long/url"
   }
   ```
   - Нажмите "Execute"
   - Получите ответ с алиасом и метаданными

3. Для получения информации о URL:
   - Найдите эндпоинт GET /urls/{alias}
   - Введите полученный алиас
   - Нажмите "Execute"
   - Получите информацию о URL и количестве переходов

4. Для проверки редиректа:
   - Найдите эндпоинт GET /{alias}
   - Введите алиас
   - Нажмите "Execute"
   - Получите редирект на оригинальный URL

### Тестирование через curl

1. Создание короткого URL:
```bash
curl -X POST "http://localhost:8000/urls/" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://example.com/very/long/url"}'
```

2. Получение информации о URL:
```bash
curl "http://localhost:8000/urls/{alias}"
```

3. Редирект на оригинальный URL:
```bash
curl -L "http://localhost:8000/{alias}"
```

## Лицензия

MIT 