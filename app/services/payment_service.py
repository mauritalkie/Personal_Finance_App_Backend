from sqlalchemy.orm import Session
from schemas.payment import PaymentCreate, PaymentEdit
from models.payment import Payment
from typing import List
from datetime import datetime

def get_all_payments(db: Session) -> List[Payment]:
    return db.query(Payment).all()

def get_payment_by_id(db: Session, payment_id: int) -> Payment:
    return db.query(Payment).filter(Payment.payment_id == payment_id).first()

def get_payments_by_user_id(db: Session, user_id: int) -> List[Payment]:
    return db.query(Payment).filter(Payment.user_id == user_id).all()

def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    db_payment = Payment(
        user_id = payment.user_id,
        amount = payment.amount,
        saving = payment.saving,
        housing = payment.housing,
        personal = payment.personal,
        concept = payment.concept,
        payment_date = payment.payment_date
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment

def update_payment(db: Session, db_payment: Payment, payment: PaymentEdit) -> Payment:

    db_payment.amount = payment.amount
    db_payment.saving = payment.saving
    db_payment.housing = payment.housing
    db_payment.personal = payment.personal
    db_payment.concept = payment.concept
    db_payment.payment_date = payment.payment_date
    db_payment.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_payment)

    return db_payment

def delete_payment(db: Session, db_payment: Payment) -> Payment:
    db.delete(db_payment)
    db.commit()
    return db_payment