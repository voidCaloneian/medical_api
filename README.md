﻿REST API для медицинской информационной системы.

## Структура репозитория
1. `tests` = <./src/api/tests.py>
2. `code` = <./src/>
3. `docker` = <./Dockerfile>
4. `migrations` = <./src/api/migrations/>

## Инструкция по локальному запуску
```
docker build -t mad_dev .
docker run -p 8000:8000 mad_dev
```

# Тесты запустятся автоматически, их отчёт будет написан при запуске самого сервера в контейнере, миграции будут также проведены.

## Аутентификация
API использует JWT (JSON Web Token) для аутентификации. Все защищенные эндпоинты требуют токен в заголовке (Headers):
```
Authorization: Bearer <your_token>
```

## Эндпоинты

# Хост используйте при запросах любой на выбор:
- localhost:8000
- 0.0.0.0:8000
- 127.0.0.1:8000

## В базу данных уже добавлен доктор, данные для авторизации ниже:
{
    "username": "test@doctor.com",
    "password": "test123"
}

### Аутентификация

#### POST /api/login/
Получение JWT токена для доступа к API.

**Request Body:**
```json
{
    "username": "test@doctor.com",
    "password": "test123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Пациенты

#### GET /api/patients/
Получение списка всех пациентов. Доступно только для пользователей с ролью врача.

**Headers:**
```
Authorization: Bearer <your_token>
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "date_of_birth": "1990-01-15",
        "diagnoses": {
            "primary": "Гипертония",
            "secondary": "Диабет"
        },
        "created_at": "2025-01-25T05:58:26.515035Z"
    },
    {
        "id": 2,
        "date_of_birth": "1985-05-20",
        "diagnoses": {
            "primary": "Астма",
            "secondary": "Бронхит"
        },
        "created_at": "2025-01-25T05:58:26.520165Z"
    },
    {
        "id": 3,
        "date_of_birth": "1995-12-03",
        "diagnoses": {
            "primary": "Мигрень",
            "secondary": "Остеохондроз"
        },
        "created_at": "2025-01-25T05:58:26.525245Z"
    }
]
```

**Response (403 Forbidden):**
```json
{
    "detail": "Доступ запрещен"
}
```

## Модели данных

### Patient (Пациент)
| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Уникальный идентификатор |
| date_of_birth | Date | Дата рождения |
| diagnoses | JSON | Диагнозы пациента |
| created_at | DateTime | Дата создания записи |

## Коды ответов
- 200: Успешный запрос
- 401: Ошибка аутентификации
- 403: Доступ запрещен
- 404: Ресурс не найден
- 500: Внутренняя ошибка сервера

## Ограничения
- Все защищенные эндпоинты требуют валидный JWT токен
- Доступ к данным пациентов имеют только пользователи с ролью врача
