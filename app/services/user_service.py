from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User
from typing import List
from datetime import datetime

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        hashed_password=user.password  # TODO: hash the password before saving it
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_user(db: Session, db_user: User, user: UserCreate) -> User:

    db_user.username = user.username
    db_user.hashed_password = user.password  # TODO: hash the password before saving it
    db_user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session, db_user: User) -> User:
    db.delete(db_user)
    db.commit()
    return db_user