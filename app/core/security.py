# from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
from core.config import settings
from pwdlib import PasswordHash

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = PasswordHash(hashers="bcrypt").recommended()

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

def hash_password(password: str) -> str:
    # return pwd_context.hash(password)
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # return pwd_context.verify(plain_password, hashed_password)
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt