# Библиотечная информационная система (Backend)

Это backend-часть информационной системы для библиотеки, разработанная с использованием современного стека технологий Python.

## 🛠 Технологический стек

- **Фреймворк**: FastAPI
- **ORM**: SQLAlchemy (async)
- **Аутентификация**: JWT (JSON Web Tokens)
- **Хеширование паролей**: bcrypt
- **Валидация данных**: Pydantic
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker
- **Мониторинг**: [https://github.com/maheshmahadevan/docker-monitoring-windows](https://github.com/maheshmahadevan/docker-monitoring-windows)

## 📌 Функциональность

- Управление книгами (CRUD)
- Управление авторами
- Управление пользователями
- Система аутентификации и авторизации
- Поиск и фильтрация книг
- Выдача и возврат книг

## 🚀 Установка и запуск

### Предварительные требования

- Python 3.12+
- PostgreSQL 16+

### Инструкция по установке

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/konstantin2710204/library-backend-project.git
   cd library-backend-project
   ```

2. Установите зависимости:
   ```bash
   pip install -r requierements.txt
   ```

3. Создайте файл `.env` на основе и заполните необходимые переменные окружения:
   ```ini
   SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@172.17.0.2:5432/library_db
   SECRET_KEY=your-secret-key
   ```

5. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## 📚 Документация API

После запуска приложения документация API будет доступна по адресам:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🧑‍💻 Разработка

### Структура проекта

```
.
├── app/                   # Основное приложение
│   ├── auth.py            # Логика аутентификации
│   ├── crud.py            # Операции CRUD
│   ├── database.py        # Работа с базой данных
│   ├── main.py            # Точка входа
│   ├── models.py          # Модели SQLAlchemy
│   └── schemas.py         # Схемы PyDantic
├── requirements.txt       # Зависимости приложения
└── README.md              # Этот файл
```
