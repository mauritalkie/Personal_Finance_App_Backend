from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from schemas.expense_type import ExpenseTypeResponse

class ExpenseBase(BaseModel):
    expense_type_id: int
    concept: str
    amount: Decimal
    expense_date: date

class ExpenseCreate(ExpenseBase):
    user_id: int

class ExpenseEdit(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    expense_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode=True

class ExpenseDetailResponse(ExpenseResponse):
    expense_type: str