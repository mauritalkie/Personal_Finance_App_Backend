from fastapi import FastAPI, Depends
from api.router import api_router
from typing import Annotated
from dependencies import oauth2_scheme
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(api_router)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "Hello, World!"}