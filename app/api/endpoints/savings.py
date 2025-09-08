from fastapi import APIRouter, Depends, status, HTTPException
from dependencies import get_current_user, get_db
from schemas.saving import LeftSavingsResponse
from sqlalchemy.orm import Session
from services import saving_service

router = APIRouter(
    tags=["savings"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)

@router.get("/savings", response_model=LeftSavingsResponse, status_code=status.HTTP_200_OK)
def get_savings(user_id: int, db: Session = Depends(get_db)):
    savings = saving_service.get_savings_by_user_id(db, user_id)

    if savings is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Some of the expenses types are missing"
        )
    
    return savings