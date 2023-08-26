from fastapi import APIRouter

from .users import router as users_router
from .logs import router as logs_router

api_router = APIRouter(prefix="/api")

api_router.include_router(logs_router, prefix="/logs", tags=["Log"])

api_router.include_router(users_router)
