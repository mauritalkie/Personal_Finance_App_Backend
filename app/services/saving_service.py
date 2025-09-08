from sqlalchemy.orm import Session
from schemas.saving import LeftSavingsResponse
from typing import List
from models.expense_type import ExpenseType
from services.expense_type_service import get_expenses_types_by_user_id
from models.expense import Expense
from models.payment import Payment
from sqlalchemy import func

def get_savings_by_user_id(db: Session, user_id: int) -> LeftSavingsResponse | None:

    expensesTypes: List[ExpenseType] = get_expenses_types_by_user_id(db, user_id)

    matches = [et.expense_type_id for et in expensesTypes if et.expense_type.lower() in 'personal']
    personal_id = matches[0] if matches else None

    matches = [et.expense_type_id for et in expensesTypes if et.expense_type.lower() in 'housing']
    housing_id = matches[0] if matches else None

    matches = [et.expense_type_id for et in expensesTypes if et.expense_type.lower() in 'saving']
    saving_id = matches[0] if matches else None

    if personal_id is None or housing_id is None or saving_id is None:
        return None

    total_personal_expense = db.query(Expense).filter(Expense.user_id == user_id, Expense.expense_type_id == personal_id).with_entities(func.sum(Expense.amount)).scalar()
    total_housing_expense = db.query(Expense).filter(Expense.user_id == user_id, Expense.expense_type_id == housing_id).with_entities(func.sum(Expense.amount)).scalar()
    total_saving_expense = db.query(Expense).filter(Expense.user_id == user_id, Expense.expense_type_id == saving_id).with_entities(func.sum(Expense.amount)).scalar()

    total_personal_payment = db.query(Payment).filter(Payment.user_id == user_id).with_entities(func.sum(Payment.personal)).scalar()
    total_housing_payment = db.query(Payment).filter(Payment.user_id == user_id).with_entities(func.sum(Payment.housing)).scalar()
    total_saving_payment = db.query(Payment).filter(Payment.user_id == user_id).with_entities(func.sum(Payment.saving)).scalar()

    return LeftSavingsResponse(
        personal = (total_personal_payment or 0) - (total_personal_expense or 0),
        housing = (total_housing_payment or 0) - (total_housing_expense or 0),
        saving = (total_saving_payment or 0) - (total_saving_expense or 0)
    )