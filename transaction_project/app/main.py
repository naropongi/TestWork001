from app.router import router as transaction_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(transaction_router)
