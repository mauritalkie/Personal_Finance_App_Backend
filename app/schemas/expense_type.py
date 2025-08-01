from pydantic import BaseModel
from datetime import datetime

class ExpenseTypeBase(BaseModel):
    expense_type: str
    expense_percentage: int

class ExpenseTypeCreate(ExpenseTypeBase):
    user_id: int

class ExpenseTypeEdit(ExpenseTypeBase):
    pass

class ExpenseTypeResponse(ExpenseTypeBase):
    expense_type_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True