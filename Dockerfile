FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода и скрипта запуска
COPY . .
COPY start.sh /app/start.sh

# Создание непривилегированного пользователя
RUN useradd -m appuser && chown -R appuser:appuser /app
RUN chmod +x /app/start.sh
USER appuser

# Запуск приложения
CMD ["/app/start.sh"] 