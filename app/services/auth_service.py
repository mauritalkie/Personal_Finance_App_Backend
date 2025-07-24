from sqlalchemy.orm import Session
from models.user import User as UserModel
from services import user_service
from core.security import verify_password

def authenticate_user(db: Session, username: str, password: str) -> UserModel | None:
    user = user_service.get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
