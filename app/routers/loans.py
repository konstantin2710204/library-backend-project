from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal
from app.schemas import BookCopyCreateSchema, User
from app.auth import get_current_user
from sqlalchemy.orm import Session

from app import schemas
from app import crud
from app import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.expire_all()

@router.post("/loans/new", response_model=schemas.LoanCreate)
def get_readers(
    current_user: Annotated[User, Depends(get_current_user)],
    loan_data: schemas.LoanCreate,
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.book_name == loan_data.book_name).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    # Check for an available book copy
    available_copy = db.query(models.BookCopy).filter(
        models.BookCopy.book_id == book.book_id, 
        models.BookCopy.status == "Доступна"
    ).first()

    if not available_copy:
        raise HTTPException(status_code=400, detail="No available copy for this book.")

    # Create new Loan instance
    new_loan = models.Loan(
        loan_date=date.today(),
        due_date=loan_data.due_date,
        copy_id=available_copy.copy_id
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    # Update the status of the book copy to 'На руках'
    available_copy.status = "На руках"
    db.commit()

    # Associate the loan with a user card
    user_card = db.query(models.UserCard).filter(models.UserCard.user_id == loan_data.user_id).first()
    if user_card:
        user_card.loan_id = new_loan.loan_id
        db.commit()

    return loan_data