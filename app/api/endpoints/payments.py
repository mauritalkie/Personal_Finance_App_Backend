from fastapi import APIRouter, status, HTTPException, Depends, Query
from schemas.payment import PaymentCreate, PaymentResponse, PaymentEdit
from typing import List, Optional
from models.payment import Payment as PaymentModel
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from services import payment_service

router = APIRouter(
    tags=["payments"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)

@router.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db, payment)

@router.get("/payments", response_model=List[PaymentResponse], status_code=200)
def get_payments(user_id: Optional[int] = Query(None) ,db: Session = Depends(get_db)):
    if user_id is not None:
        return payment_service.get_payments_by_user_id(db, user_id)
    return payment_service.get_all_payments(db)

@router.get("/payments/{payment_id}", response_model=PaymentResponse, status_code=200)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = payment_service.get_payment_by_id(db, payment_id)

    if db_payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return db_payment

@router.put("/payments/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
def update_expense_type(payment_id: int, payment_type: PaymentEdit, db: Session = Depends(get_db)):
    db_payment = payment_service.get_payment_by_id(db, payment_id)

    if db_payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment_service.update_payment(db, db_payment, payment_type)

@router.delete("/payments/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = payment_service.get_payment_by_id(db, payment_id)

    if db_payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment_service.delete_payment(db, db_payment)