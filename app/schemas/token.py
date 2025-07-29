from pydantic import BaseModel

class TokenBase(BaseModel):
    refresh_token: str

class TokenResponse(TokenBase):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None