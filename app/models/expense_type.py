from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.base import Base

class ExpenseType(Base):
    __tablename__ = "expenses_types"

    expense_type_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    expense_type = Column(Text, nullable=False)
    expense_percentage = Column(Integer, nullable=False)

    user = relationship("User", back_populates="expense_types")
    expenses = relationship("Expense", back_populates="expense_type", cascade="all, delete-orphan")
