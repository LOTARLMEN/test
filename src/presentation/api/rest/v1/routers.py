from fastapi import APIRouter
from src.presentation.api.rest.v1.controllers.wallet import router as wallet_router

v1_router = APIRouter()

v1_router.include_router(wallet_router)
