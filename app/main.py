from fastapi import FastAPI, Depends
from api.router import api_router
from typing import Annotated
from dependencies import oauth2_scheme

app = FastAPI()

app.include_router(api_router)

@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "Hello, World!"}