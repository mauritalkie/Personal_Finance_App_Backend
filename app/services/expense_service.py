from sqlalchemy.orm import Session
from schemas.expense import ExpenseCreate, ExpenseEdit, ExpenseResponse
from models.expense import Expense
from typing import List
from datetime import datetime
from sqlalchemy import desc
from models.expense_type import ExpenseType

def get_all_expenses(db: Session) -> List[Expense]:
    expenses = (
        db.query(Expense, ExpenseType)
        .join(ExpenseType, Expense.expense_type_id == ExpenseType.expense_type_id)
        .order_by(desc(Expense.expense_id))
        .all()
    )

    return [
        ExpenseResponse (
            expense_id=expense.Expense.expense_id,
            user_id=expense.Expense.user_id,
            expense_type_id=expense.Expense.expense_type_id,
            concept=expense.Expense.concept,
            amount=expense.Expense.amount,
            expense_date=expense.Expense.expense_date,
            created_at=expense.Expense.created_at,
            updated_at=expense.Expense.updated_at,
            expense_type=expense.ExpenseType.expense_type
        )
        for expense in expenses
    ]

def get_expense_by_id(db: Session, expense_id: int) -> Expense:
    expense = (
        db.query(Expense, ExpenseType)
        .join(ExpenseType, Expense.expense_type_id == ExpenseType.expense_type_id)
        .filter(Expense.expense_id == expense_id)
        .first()
    )

    return ExpenseResponse (
        expense_id=expense.Expense.expense_id,
        user_id=expense.Expense.user_id,
        expense_type_id=expense.Expense.expense_type_id,
        concept=expense.Expense.concept,
        amount=expense.Expense.amount,
        expense_date=expense.Expense.expense_date,
        created_at=expense.Expense.created_at,
        updated_at=expense.Expense.updated_at,
        expense_type=expense.ExpenseType.expense_type
    )

def get_expenses_by_user_id(db: Session, user_id: int) -> List[Expense]:
    expenses = (
        db.query(Expense, ExpenseType)
        .join(ExpenseType, Expense.expense_type_id == ExpenseType.expense_type_id)
        .filter(Expense.user_id == user_id)
        .order_by(desc(Expense.expense_id))
        .all()
    )

    return [
        ExpenseResponse (
            expense_id=expense.Expense.expense_id,
            user_id=expense.Expense.user_id,
            expense_type_id=expense.Expense.expense_type_id,
            concept=expense.Expense.concept,
            amount=expense.Expense.amount,
            expense_date=expense.Expense.expense_date,
            created_at=expense.Expense.created_at,
            updated_at=expense.Expense.updated_at,
            expense_type=expense.ExpenseType.expense_type
        )
        for expense in expenses
    ]

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