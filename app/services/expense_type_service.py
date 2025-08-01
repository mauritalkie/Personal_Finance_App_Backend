from sqlalchemy.orm import Session
from schemas.expense_type import ExpenseTypeCreate, ExpenseTypeEdit
from models.expense_type import ExpenseType
from typing import List
from datetime import datetime

def get_all_expenses_types(db: Session) -> List[ExpenseType]:
    return db.query(ExpenseType).all()

def get_expense_type_by_id(db: Session, expense_type_id: int) -> ExpenseType:
    return db.query(ExpenseType).filter(ExpenseType.expense_type_id == expense_type_id).first()

def get_expenses_types_by_user_id(db: Session, user_id: int) -> List[ExpenseType]:
    return db.query(ExpenseType).filter(ExpenseType.user_id == user_id).all()

def get_expense_type_by_name_and_user_id(db: Session, expense_type: str, user_id: int) -> ExpenseType:
    return db.query(ExpenseType).filter(
        ExpenseType.expense_type == expense_type,
        ExpenseType.user_id == user_id
    ).first()

def create_expense_type(db: Session, expense_type: ExpenseTypeCreate) -> ExpenseType:
    db_expense_type = ExpenseType(
        user_id = expense_type.user_id,
        expense_type = expense_type.expense_type,
        expense_percentage = expense_type.expense_percentage
    )

    db.add(db_expense_type)
    db.commit()
    db.refresh(db_expense_type)

    return db_expense_type

def update_expense_type(db: Session, db_expense_type: ExpenseType, expense_type: ExpenseTypeEdit) -> ExpenseType:

    db_expense_type.expense_type = expense_type.expense_type
    db_expense_type.expense_percentage = expense_type.expense_percentage
    db_expense_type.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_expense_type)

    return db_expense_type

def delete_expense_type(db: Session, db_expense_type: ExpenseType) -> ExpenseType:
    db.delete(db_expense_type)
    db.commit()
    return db_expense_type