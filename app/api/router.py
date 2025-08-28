from fastapi import APIRouter
from api.endpoints import users, auth, expenses_types, payments, expenses

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(expenses_types.router)
api_router.include_router(payments.router)
api_router.include_router(expenses.router)