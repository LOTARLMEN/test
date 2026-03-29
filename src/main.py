from fastapi import FastAPI
import uvicorn
from src.presentation.api.rest.v1.routers import v1_router as wallet_router

app = FastAPI()

app.include_router(wallet_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8000)
