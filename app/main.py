from fastapi import FastAPI
from schemas.user import User
from api.router import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}