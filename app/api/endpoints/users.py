from fastapi import APIRouter, status, HTTPException, Depends
from schemas.user import UserCreate, UserOut
from typing import List
from models.user import User as UserModel
from sqlalchemy.orm import Session
from dependencies import get_db
from datetime import datetime

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = UserModel(
        username=user.username,
        hashed_password=user.password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()

    return new_user

@router.get("/users", response_model=List[UserOut], status_code=200)
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get("/users/{user_id}", response_model=UserOut, status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    return db_user

@router.put("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_user.username = user.username
    db_user.hashed_password = user.password
    db_user.updated_at = datetime.utcnow()

    db.commit()
    return db_user

@router.delete("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()
    return db_user