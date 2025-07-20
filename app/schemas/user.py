from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime