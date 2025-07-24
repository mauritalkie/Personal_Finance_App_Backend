from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from db.base import Base

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    expense_type_id = Column(Integer, ForeignKey("expenses_types.expense_type_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(6, 2), nullable=False)

    user = relationship("User", back_populates="expenses")
    expense_type = relationship("ExpenseType", back_populates="expenses")
