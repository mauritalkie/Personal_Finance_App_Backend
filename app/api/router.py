from fastapi import APIRouter
from api.endpoints import users, auth

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(auth.router)