from fastapi import APIRouter, status, HTTPException, Depends
from schemas.user import UserCreate, UserOut
from typing import List
from models.user import User as UserModel
from sqlalchemy.orm import Session
from dependencies import get_db
from services import user_service

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_username(db, user.username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    return user_service.create_user(db, user)

@router.get("/users", response_model=List[UserOut], status_code=200)
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get("/users/{user_id}", response_model=UserOut, status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db_user

@router.put("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_service.update_user(db, db_user, user)

@router.delete("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user_service.delete_user(db, db_user)