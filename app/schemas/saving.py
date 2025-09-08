from pydantic import BaseModel
from decimal import Decimal

class LeftSavingsResponse(BaseModel):
    personal: Decimal
    housing: Decimal
    saving: Decimal

    class Config:
        orm_mode = True