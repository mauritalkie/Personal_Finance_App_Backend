from sqlalchemy.orm import Session
from schemas.expense import ExpenseCreate, ExpenseEdit
from models.expense import Expense
from typing import List
from datetime import datetime

def get_all_expenses(db: Session) -> List[Expense]:
    return db.query(Expense).all()

def get_expense_by_id(db: Session, expense_id: int) -> Expense:
    return db.query(Expense).filter(Expense.expense_id == expense_id).first()

def get_expenses_by_user_id(db: Session, user_id: int) -> List[Expense]:
    return db.query(Expense).filter(Expense.user_id == user_id).all()

def create_expense(db: Session, expense: ExpenseCreate) -> Expense:
    db_expense = Expense(
        user_id = expense.user_id,
        expense_type_id = expense.expense_type_id,
        concept = expense.concept,
        amount = expense.amount,
        expense_date = expense.expense_date
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense

def update_expense(db: Session, db_expense: Expense, expense: ExpenseEdit) -> Expense:

    db_expense.expense_type_id = expense.expense_type_id
    db_expense.concept = expense.concept
    db_expense.amount = expense.amount
    db_expense.expense_date = expense.expense_date
    db_expense.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_expense)

    return db_expense

def delete_expense(db: Session, db_expense: Expense) -> Expense:
    db.delete(db_expense)
    db.commit()
    return db_expense