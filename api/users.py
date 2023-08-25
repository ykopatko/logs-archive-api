from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from core.user_manager import get_user_manager
from models.users import User
from serializers.users import UserRead, UserCreate, UserUpdate
from utils.auth import auth_backend


router = APIRouter()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
