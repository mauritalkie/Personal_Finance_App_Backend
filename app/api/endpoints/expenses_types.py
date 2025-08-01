from fastapi import APIRouter, status, HTTPException, Depends, Query
from schemas.expense_type import ExpenseTypeCreate, ExpenseTypeResponse, ExpenseTypeEdit
from typing import List, Optional
from models.expense_type import ExpenseType as ExpenseTypeModel
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from services import expense_type_service

router = APIRouter(
    tags=["expenses_types"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)

@router.post("/expenses_types", response_model=ExpenseTypeResponse, status_code=status.HTTP_201_CREATED)
def create_expense_type(expense_type: ExpenseTypeCreate, db: Session = Depends(get_db)):
    existing_expense_type = expense_type_service.get_expense_type_by_name_and_user_id(
        db, expense_type.expense_type, expense_type.user_id
    )

    if existing_expense_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense type already exists"
        )
    
    return expense_type_service.create_expense_type(db, expense_type)

@router.get("/expenses_types", response_model=List[ExpenseTypeResponse], status_code=200)
def get_expenses_types(user_id: Optional[int] = Query(None) ,db: Session = Depends(get_db)):
    if user_id is not None:
        return expense_type_service.get_expenses_types_by_user_id(db, user_id)
    return expense_type_service.get_all_expenses_types(db)

@router.get("/expenses_types/{expense_type_id}", response_model=ExpenseTypeResponse, status_code=200)
def get_expense_type(expense_type_id: int, db: Session = Depends(get_db)):
    db_expense_type = expense_type_service.get_expense_type_by_id(db, expense_type_id)

    if db_expense_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense type not found"
        )
    
    return db_expense_type

@router.put("/expenses_types/{expense_type_id}", response_model=ExpenseTypeResponse, status_code=status.HTTP_200_OK)
def update_expense_type(expense_type_id: int, expense_type: ExpenseTypeEdit, db: Session = Depends(get_db)):
    db_expense_type = expense_type_service.get_expense_type_by_id(db, expense_type_id)

    if db_expense_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense type not found"
        )
    
    return expense_type_service.update_expense_type(db, db_expense_type, expense_type)

@router.delete("/expenses_types/{expense_type_id}", response_model=ExpenseTypeResponse, status_code=status.HTTP_200_OK)
def delete_expense_type(expense_type_id: int, db: Session = Depends(get_db)):
    db_expense_type = expense_type_service.get_expense_type_by_id(db, expense_type_id)

    if db_expense_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense type not found"
        )

    return expense_type_service.delete_expense_type(db, db_expense_type)