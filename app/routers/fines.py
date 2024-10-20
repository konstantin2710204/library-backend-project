from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.auth import get_current_user
from app.database import SessionLocal
from app.models import Fine
from app.schemas import User, FineUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.expire_all()

# Маршрут для получения списка всех штрафов
@router.get("/fines", response_model=List[schemas.FineInfo])
def get_fines(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    fine_cards = crud.get_fines(db=db)

    return [
        schemas.FineInfo(
            fine_id=fine_card.fine.fine_id,
            user_name=f"{fine_card.user.user_lname} {fine_card.user.user_fname} {fine_card.user.user_mname}",
            user_email=fine_card.user.user_email,
            fine_amount=fine_card.fine.fine_amount,
            date_received=fine_card.fine.fine_date,
            unreturned_books=[
                book.book_name for book in crud.get_unreturned_books_for_user(db=db, user_id=fine_card.user.user_id)
            ],
            paid=fine_card.fine.fine_paid,
        )
        for fine_card in fine_cards
    ]

# Маршрут для получения информации о конкретном штрафе по ID
@router.get("/fines/{fine_id}", response_model=schemas.FineInfo)
def get_fine_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    fine_id: int,
    db: Session = Depends(get_db)
):
    fine_card = crud.get_fine(db=db, fine_id=fine_id)
    if fine_card is None:
        raise HTTPException(status_code=404, detail="Fine not found")
    return schemas.FineInfo(
        fine_id=fine_card.fine.fine_id,
        user_name=f"{fine_card.user.user_lname} {fine_card.user.user_fname} {fine_card.user.user_mname}",
        user_email=fine_card.user.user_email,
        fine_amount=fine_card.fine.fine_amount,
        date_received=fine_card.fine.fine_date,
        unreturned_books=[
            book.book_name for book in crud.get_unreturned_books_for_user(db=db, user_id=fine_card.user.user_id)
        ],
        paid=fine_card.fine.fine_paid,
    )

@router.patch("/fines/{fine_id}", response_model=schemas.FineUpdate)
def update_fine(
    current_user: Annotated[User, Depends(get_current_user)],
    fine_id: int,
    fine_data: FineUpdate,
    db: Session = Depends(get_db)
):
    try:
        fine = db.query(Fine).filter(Fine.fine_id == fine_id).first()
        if not fine:
            raise HTTPException(status_code=404, detail="Fine not found")

        update_data = fine_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(fine, key, value)

        db.commit()
        db.refresh(fine)

        return fine

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/fines/{fine_id}", status_code=204)
def delete_fine_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    fine_id: int,
    db: Session = Depends(get_db),
):
    try:
        fine = db.query(Fine).filter(Fine.fine_id == fine_id).first()
        if not fine:
            raise HTTPException(status_code=404, detail="Fine not found")

        db.delete(fine)
        db.commit()

        return {"detail": "Fine deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

