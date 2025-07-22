from fastapi import APIRouter, status, HTTPException
from schemas.user import User
from db.database import SessionLocal
from typing import List
from models.user import User as UserModel

db = SessionLocal()

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):

    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = UserModel(
        username=user.username,
        hashed_password=user.hashed_password,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    db.add(new_user)
    db.commit()

    return new_user

@router.get("/users", response_model=List[User], status_code=200)
def get_users():
    users = db.query(UserModel).all()
    return users

@router.get("/users/{user_id}", response_model=User, status_code=200)
def get_user(user_id: int):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    return db_user

@router.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_user.username = user.username
    db_user.hashed_password = user.hashed_password
    db_user.updated_at = user.updated_at

    db.commit()
    return db_user

@router.delete("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()
    return db_user