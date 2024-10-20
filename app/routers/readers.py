from math import expm1
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic.v1 import NoneStr
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.auth import get_current_user
from app.crud import create_reader
from app.database import SessionLocal
from app.models import UserCard, FineCard, BookCopy, Book
from app.schemas import User, Reader, ReaderCreate, ReaderUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.expire_all()

# Маршрут для получения списка пользователей
@router.get("/readers", response_model=List[schemas.UserInfo])
def get_readers(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    users = db.query(UserCard).all()

    return [
        schemas.UserInfo(
            user_id=user.user_id,
            user_name=f"{user.user_lname} {user.user_fname} {user.user_mname}",
            user_email=user.user_email,
            registration_date=user.registration_date,
            borrowed_books=[
                f"{book.book_name}"
                for book in db.query(Book).join(BookCopy).filter(BookCopy.copy_id == user.loan_id)
            ],
            fines=sum(fine.fine_amount for fine in user.fines),
            status=user.status,
        )
        for user in users
    ]

# Маршрут для получения информации о пользователе по ID
@router.get("/readers/{reader_id}", response_model=schemas.UserInfo)
def get_reader_by_id(
    reader_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(UserCard).filter(UserCard.user_id == reader_id).first()

    return schemas.UserInfo(
        user_id=user.user_id,
        user_name=f"{user.user_lname} {user.user_fname} {user.user_mname}",
        user_email=user.user_email,
        registration_date=user.registration_date,
        borrowed_books=[
            f"{book.book_name}"
            for book in db.query(Book).join(BookCopy).filter(BookCopy.copy_id == user.loan_id)
        ],
        fines=sum(fine.fine_amount for fine in user.fines),
        status=user.status,
    )

@router.post("/readers/new", response_model=Reader)
def add_reader(
    current_user: Annotated[User, Depends(get_current_user)],
    reader: ReaderCreate,
    db: Session = Depends(get_db)
):

    return create_reader(db=db, reader=reader)

@router.patch("/readers/{reader_id}", response_model=ReaderUpdate)
def update_reader(
    current_user: Annotated[User, Depends(get_current_user)],
    reader_id: int,
    user_data: ReaderUpdate,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(UserCard).filter(UserCard.user_id == reader_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Reader not found")

        update_data = user_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/readers/{reader_id}", status_code=204)
def delete_reader(
    current_user: Annotated[User, Depends(get_current_user)],
    reader_id: int,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(UserCard).filter(UserCard.user_id == reader_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Reader not found")

        db.delete(user)
        db.commit()

        return {"detail": "Reader deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))