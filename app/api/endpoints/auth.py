from fastapi import APIRouter, status, HTTPException, Depends
from schemas.user import UserCreate, UserOut
from schemas.token import Token, TokenBase
from typing import List, Annotated
from models.user import User as UserModel
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from services.auth_service import authenticate_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core import security
from datetime import timedelta
from services import user_service

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
    refresh_token_expires = timedelta(minutes=security.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )

    refresh_token = security.create_access_token(
        data={"sub": user.username}, 
        expires_delta=refresh_token_expires
    )
    
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/refresh-token", response_model=Token, status_code=status.HTTP_200_OK)
def refresh_token(refresh_token: TokenBase, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token: str = refresh_token.refresh_token

    try:
        payload = security.jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except security.InvalidTokenError:
        raise credentials_exception

    user = user_service.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=security.REFRESH_TOKEN_EXPIRE_MINUTES)

    new_access_token = security.create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )

    new_refresh_token = security.create_access_token(
        data={"sub": user.username}, 
        expires_delta=refresh_token_expires
    )

    return Token(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")