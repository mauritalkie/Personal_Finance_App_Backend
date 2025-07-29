from sqlalchemy import Column, Integer, ForeignKey, Numeric, Text, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import date
from db.base import Base
from datetime import datetime


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(6, 2), nullable=False)
    saving = Column(Numeric(6, 2), nullable=False)
    housing = Column(Numeric(6, 2), nullable=False)
    personal = Column(Numeric(6, 2), nullable=False)
    concept = Column(Text, nullable=False)
    payment_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")
