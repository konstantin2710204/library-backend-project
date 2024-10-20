from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import auth
from app.models import Base
from app.database import engine, SessionLocal
from app.routers import books, readers, fines, loans

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Разрешенные источники для CORS (можно указать конкретные домены вместо "*")
origins = [
    "*"
]

# Middleware для обработки CORS-запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Маршрут для проверки работы API
@app.get("/")
def read_root():
    return {"message": "Welcome to the Library API"}

# Подключение маршрутов для работы с книгами
app.include_router(books.router, prefix="/api", tags=["books"])

# Подключение маршрутов для работы с пользователями
app.include_router(readers.router, prefix="/api", tags=["readers"])

# Подключение маршрутов для работы с штрафами
app.include_router(fines.router, prefix="/api", tags=["fines"])

app.include_router(loans.router, prefix="/api", tags=["loans"])

app.include_router(auth.router, tags=["auth"])