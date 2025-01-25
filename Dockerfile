# Используем компактный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Настраиваем Poetry и устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем исходный код проекта
COPY . .

# Открываем порт для приложения
EXPOSE 8000
RUN echo "PYTHONPATH is $PYTHONPATH"

WORKDIR /app/src

# Запускаем тесты, миграции и сам сервер
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && coverage run manage.py test && coverage report && python manage.py seed_data && python manage.py runserver 0.0.0.0:8000"]
