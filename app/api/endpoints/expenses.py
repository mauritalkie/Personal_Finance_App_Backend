from datetime import date
from fastapi import APIRouter, status, HTTPException, Depends, Query
from schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseEdit, ExpenseDetailResponse
from typing import List, Optional
from models.expense import Expense as ExpenseModel
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from services import expense_service

router = APIRouter(
    tags=["expenses"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)

@router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return expense_service.create_expense(db, expense)

@router.get("/expenses", response_model=List[ExpenseDetailResponse], status_code=200)
def get_expenses(user_id: int = Query(...), start_date: Optional[date] = Query(None), end_date: Optional[date] = Query(None), db: Session = Depends(get_db)):
    return expense_service.get_expenses_by_filters(db, user_id, start_date, end_date)

@router.get("/expenses/{expense_id}", response_model=ExpenseDetailResponse, status_code=200)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = expense_service.get_expense_by_id(db, expense_id)

    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="expense not found"
        )
    
    return db_expense

@router.put("/expenses/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def update_expense_type(expense_id: int, expense_type: ExpenseEdit, db: Session = Depends(get_db)):
    db_expense = expense_service.get_expense_model_by_id(db, expense_id)

    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="expense not found"
        )
    
    return expense_service.update_expense(db, db_expense, expense_type)

@router.delete("/expenses/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = expense_service.get_expense_model_by_id(db, expense_id)

    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="expense not found"
        )

    return expense_service.delete_expense(db, db_expense)