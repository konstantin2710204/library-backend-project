from typing import Annotated, List
from unicodedata import category

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.crud import get_category, get_genre
from app.database import SessionLocal
from app.auth import get_current_user
from app.models import Category, Publisher, Book, BookCopy, Genre, AuthorBook, Author, BookLocation, Loan
from app.schemas import User, BookCopyInfo, BookCopyCreateSchema, BookCopyUpdateSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.expire_all()

# Маршрут для получения списка книг
@router.get("/books", response_model=List[schemas.BookCopyInfo])
def get_book_copies(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    book_locations = crud.get_books(db=db)

    return [
        schemas.BookCopyInfo(
            copy_id=book_location.copy.copy_id,
            book=book_location.copy.book.book_name,
            genre=book_location.copy.book.genre.genre_name,
            author=[
                f"{author.author_lname} {author.author_fname} {author.author_mname or ''}".strip()
                for author in db.query(Author).join(AuthorBook).filter(AuthorBook.book_id == book_location.copy.book.book_id).all()
            ],
            book_location=f"{book_location.shelf.rack.section.section_name}, {book_location.shelf.rack.rack_name}, {book_location.shelf.shelf_number} полка",
            photo=book_location.copy.photo,
            status=book_location.copy.status,
        )
        for book_location in book_locations
    ]

# Маршрут для получения книги по ID
@router.get("/books/{copy_id}", response_model=BookCopyInfo)
def get_book_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    copy_id: int,
    db: Session = Depends(get_db),
):
    book_location = crud.get_book(db=db, copy_id=copy_id)

    if book_location is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return schemas.BookCopyInfo(
        copy_id=book_location.copy.copy_id,
        book=book_location.copy.book.book_name,
        genre=book_location.copy.book.genre.genre_name,
        author=[
            f"{author.author_lname} {author.author_fname} {author.author_mname or ''}".strip()
            for author in db.query(Author).join(AuthorBook).filter(AuthorBook.book_id == book_location.copy.book.book_id).all()
        ],
        book_location=f"{book_location.shelf.rack.section.section_name or 'Основной склад'}, {book_location.shelf.rack.rack_name or 'На складе'}, {book_location.shelf.shelf_number or 'На складе'} полка",
        photo=book_location.copy.photo,
        status=book_location.copy.status,
    )

@router.post("/books/new", response_model=schemas.BookCreateSchema)
def add_book(
    current_user: Annotated[User, Depends(get_current_user)],
    book_data: schemas.BookCreateSchema,
    db: Session = Depends(get_db)
):
    try:
        category = db.query(Category).filter(Category.category_name == book_data.category_name).first()
        if not category:
            category = Category(
                category_name=book_data.category_name,
            )
            db.add(category)
            db.flush()

        genre = db.query(Genre).filter(Genre.genre_name == book_data.genre_name).first()
        if not genre:
            genre = Genre(
                genre_name=book_data.genre_name,
            )
            db.add(genre)
            db.flush()

        new_book = Book(
            book_name=book_data.book_name,
            publishing_year=book_data.publishing_year,
            pages_number=book_data.pages_number,
            category_id=category.category_id,
            genre_id=genre.genre_id,
        )

        db.add(new_book)
        db.flush()

        author = db.query(Author).filter(Author.author_lname == book_data.author_lname).first()
        if not author:

            author = Author(
                author_lname=book_data.author_lname,
                author_fname=book_data.author_fname,
                author_mname=book_data.author_mname,
                birth_year=book_data.birth_year,
                death_year=book_data.death_year,
            )

            db.add(author)
            db.flush()

        new_author = AuthorBook(
            author_id=author.author_id,
            book_id=new_book.book_id,
        )

        db.add(new_author)
        db.flush()

        db.commit()

        return {
            "book_name": new_book.book_name,
            "publishing_year": new_book.publishing_year,
            "pages_number": new_book.pages_number,
            "category_name": new_book.category.category_name,
            "genre_name": new_book.genre.genre_name,
            "author_lname": author.author_lname,
            "author_fname": author.author_fname,
            "author_mname": author.author_mname,
            "birth_year": author.birth_year,
            "death_year": author.death_year,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/books/new/copy", response_model=BookCopyCreateSchema)
def add_book_copy(
    current_user: Annotated[User, Depends(get_current_user)],
    copy_data: schemas.BookCopyCreateSchema,
    db: Session = Depends(get_db)
):
    try:

        book = db.query(Book).filter(Book.book_name == copy_data.book_name).first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        publisher = db.query(Publisher).filter(Publisher.publisher_name == copy_data.publisher_name).first()

        if not publisher:
            publisher = Publisher(
                publisher_name=copy_data.publisher_name,
            )
            db.add(publisher)
            db.flush()

        new_copy = BookCopy(
            photo=copy_data.photo,
            book_id=book.book_id,
            publisher_id=publisher.publisher_id,
        )

        db.add(new_copy)
        db.flush()

        new_location = BookLocation(
            copy_id=new_copy.copy_id,
            shelf_id=copy_data.shelf_id,
        )

        db.add(new_location)
        db.flush()

        db.commit()

        return {
            "photo": new_copy.photo,
            "book_name": new_copy.book.book_name,
            "publisher_name": new_copy.publisher.publisher_name,
            "shelf_number": new_location.shelf.shelf_number,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/books/{copy_id}", response_model=BookCopyUpdateSchema)
def update_book(
    current_user: Annotated[User, Depends(get_current_user)],
    copy_id: int,
    book_data: BookCopyUpdateSchema,
    db: Session = Depends(get_db),
):
    try:
        book = db.query(BookCopy).filter(BookCopy.copy_id == copy_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Reader not found")

        update_data = book_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(book, key, value)

        db.commit()
        db.refresh(book)

        return book

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/books/{copy_id}", status_code=204)
def delete_book_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    copy_id: int,
    db: Session = Depends(get_db)
):
    try:
        copy = db.query(BookCopy).filter(BookCopy.copy_id == copy_id).first()
        if not copy:
            raise HTTPException(status_code=404, detail="Book not found")

        # Найти все записи, связанные с этой копией книги в таблице loans
        loans = db.query(Loan).filter(Loan.copy_id == copy_id).all()
        if loans:
            # Удалить или обработать записи из таблицы loans
            for loan in loans:
                db.delete(loan)

        # Найти все записи, связанные с этой копией книги в таблице book_locations
        book_locations = db.query(BookLocation).filter(BookLocation.copy_id == copy_id).all()
        if book_locations:
            # Удалить записи из таблицы book_locations
            for location in book_locations:
                db.delete(location)

        db.delete(copy)
        db.commit()

        return {"detail": "Book deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))