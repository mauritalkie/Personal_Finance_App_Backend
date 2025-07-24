from fastapi import APIRouter, status, HTTPException, Depends
from schemas.user import UserCreate, UserOut
from schemas.token import Token
from typing import List, Annotated
from models.user import User as UserModel
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from services.auth_service import authenticate_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core import security
from datetime import timedelta

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect username or password", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    if user is None:
        raise credentials_exception
    if not security.verify_password(form_data.password, user.hashed_password):
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")