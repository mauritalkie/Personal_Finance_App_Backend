from sqlalchemy import Column, Integer, ForeignKey, Numeric, Text, Date, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    expense_type_id = Column(Integer, ForeignKey("expenses_types.expense_type_id", ondelete="CASCADE"), nullable=False)
    concept = Column(Text, nullable=False)
    amount = Column(Numeric(7, 2), nullable=False)
    expense_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="expenses")
    expense_type = relationship("ExpenseType", back_populates="expenses")
