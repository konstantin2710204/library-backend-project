from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.models import EmployeeCredential, Loan, UserCard, FineCard
from app.schemas import UserInDB

def get_user(db: Session, username):
    return db.query(models.EmployeeCredential).filter(models.EmployeeCredential.username == username).first()

# CRUD operations for Section
def create_section(db: Session, section: schemas.SectionCreate):
    db_section = models.Section(**section.dict())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

def get_section(db: Session, section_id: int):
    return db.query(models.Section).filter(models.Section.section_id == section_id).first()

def get_sections(db: Session):
    return db.query(models.Section).all()

def update_section(db: Session, section_id: int, section: schemas.SectionCreate):
    db_section = get_section(db, section_id)
    if db_section:
        for key, value in section.dict().items():
            setattr(db_section, key, value)
        db.commit()
        db.refresh(db_section)
    return db_section

def delete_section(db: Session, section_id: int):
    db_section = get_section(db, section_id)
    if db_section:
        db.delete(db_section)
        db.commit()
    return db_section

# CRUD operations for Rack
def create_rack(db: Session, rack: schemas.RackCreate):
    db_rack = models.Rack(**rack.dict())
    db.add(db_rack)
    db.commit()
    db.refresh(db_rack)
    return db_rack

def get_rack(db: Session, rack_id: int):
    return db.query(models.Rack).filter(models.Rack.rack_id == rack_id).first()

def get_racks(db: Session):
    return db.query(models.Rack).all()

def update_rack(db: Session, rack_id: int, rack: schemas.RackCreate):
    db_rack = get_rack(db, rack_id)
    if db_rack:
        for key, value in rack.dict().items():
            setattr(db_rack, key, value)
        db.commit()
        db.refresh(db_rack)
    return db_rack

def delete_rack(db: Session, rack_id: int):
    db_rack = get_rack(db, rack_id)
    if db_rack:
        db.delete(db_rack)
        db.commit()
    return db_rack

# CRUD operations for Shelf
def create_shelf(db: Session, shelf: schemas.ShelfCreate):
    db_shelf = models.Shelf(**shelf.dict())
    db.add(db_shelf)
    db.commit()
    db.refresh(db_shelf)
    return db_shelf

def get_shelf(db: Session, shelf_id: int):
    return db.query(models.Shelf).filter(models.Shelf.shelf_id == shelf_id).first()

def get_shelfs(db: Session):
    return db.query(models.Shelf).all()

def update_shelf(db: Session, shelf_id: int, shelf: schemas.ShelfCreate):
    db_shelf = get_shelf(db, shelf_id)
    if db_shelf:
        for key, value in shelf.dict().items():
            setattr(db_shelf, key, value)
        db.commit()
        db.refresh(db_shelf)
    return db_shelf

def delete_shelf(db: Session, shelf_id: int):
    db_shelf = get_shelf(db, shelf_id)
    if db_shelf:
        db.delete(db_shelf)
        db.commit()
    return db_shelf

# CRUD operations for Author
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.author_id == author_id).first()

def get_authors(db: Session):
    return db.query(models.Author).all()

def update_author(db: Session, author_id: int, author: schemas.AuthorCreate):
    db_author = get_author(db, author_id)
    if db_author:
        for key, value in author.dict().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author

def get_category(db: Session, category_id: int):
    db.query(models.Category).filter(models.Category.category_id == category_id).first()

# CRUD operations for Genre
def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genre(db: Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.genre_id == genre_id).first()

def get_genres(db: Session):
    return db.query(models.Genre).all()

def update_genre(db: Session, genre_id: int, genre: schemas.GenreCreate):
    db_genre = get_genre(db, genre_id)
    if db_genre:
        for key, value in genre.dict().items():
            setattr(db_genre, key, value)
        db.commit()
        db.refresh(db_genre)
    return db_genre

def delete_genre(db: Session, genre_id: int):
    db_genre = get_genre(db, genre_id)
    if db_genre:
        db.delete(db_genre)
        db.commit()
    return db_genre

# CRUD operations for Book
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, copy_id: int):
    return db.query(models.BookLocation).join(models.BookCopy).join(models.Book).filter(models.BookCopy.copy_id == copy_id).first()

def get_books(db: Session):
    return db.query(models.BookLocation).join(models.BookCopy).join(models.Book).all()

def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        db.refresh(db_book)
    return db_book

# CRUD operations for Publisher
def create_publisher(db: Session, publisher: schemas.PublisherCreate):
    db_publisher = models.Publisher(**publisher.dict())
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher

def get_publisher(db: Session, publisher_id: int):
    return db.query(models.Publisher).filter(models.Publisher.publisher_id == publisher_id).first()

def get_publishers(db: Session):
    return db.query(models.Publisher).all()

def update_publisher(db: Session, publisher_id: int, publisher: schemas.PublisherCreate):
    db_publisher = get_publisher(db, publisher_id)
    if db_publisher:
        for key, value in publisher.dict().items():
            setattr(db_publisher, key, value)
        db.commit()
        db.refresh(db_publisher)
    return db_publisher

def delete_publisher(db: Session, publisher_id: int):
    db_publisher = get_publisher(db, publisher_id)
    if db_publisher:
        db.delete(db_publisher)
        db.commit()
    return db_publisher

async def create_user(db: AsyncSession, username: str, password: str, employee_id: int):
    hashed_password = hash_password(password)
    new_user = EmployeeCredential(
        username=username,
        password=hashed_password,
        employee_id=employee_id,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

def get_readers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FineCard).join(models.UserCard).offset(skip).all()

def get_reader(db: Session, reader_id: int):
    return db.query(models.FineCard).join(models.UserCard).join(models.Fine).filter(models.UserCard.user_id == reader_id).first()

def create_reader(db: Session, reader: schemas.ReaderCreate):
    db_reader = UserCard(**reader.dict())

    db.add(db_reader)
    db.flush()
    db.commit()
    return db_reader

def update_reader(db: Session, reader_id: int, user: schemas.Reader):
    db_user = get_reader(db, reader_id)
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.flush()
        db.commit()

        db.refresh(db_user)
    return db_user

def delete_reader(db: Session, reader_id: int):
    db_user = get_reader(db, reader_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def create_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = Loan(**loan.dict())

    db.add(db_loan)
    db.flush()

    db_user = UserCard(
        loan_id=db_loan.loan_id
    )

    db.add(db_user)
    db.flush()

    db.commit()
    return db_loan

# CRUD operations for Fines (filter by status)
def get_fines_by_status(db: Session, status: str):
    return db.query(models.Fine).filter(models.Fine.status == status).all()


def get_unreturned_books_for_user(db: Session, user_id: int):
    return (
        db.query(models.Book.book_name)
        .join(models.BookCopy, models.Book.book_id == models.BookCopy.book_id)
        .join(models.Loan, models.BookCopy.copy_id == models.Loan.copy_id)
        .join(models.UserCard, models.Loan.loan_id == models.UserCard.loan_id)
        .filter(models.UserCard.user_id == user_id)  # Условие для конкретного пользователя
        .filter(models.Loan.return_date == None)  # Условие для невозвращенных книг
        .all()
    )

# Получение списка штрафов по пользователю
def get_fines_by_user(db: Session, user_id: int):
    return db.query(models.Fine).filter(models.Fine.user_id == user_id).all()

# Получение списка штрафов
def get_fines(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FineCard).join(models.Fine).join(models.UserCard).offset(skip).limit(limit).all()

# Получение штрафа по ID
def get_fine(db: Session, fine_id: int):
    return db.query(models.FineCard).join(models.Fine).join(models.UserCard).filter(models.Fine.fine_id == fine_id).first()