import os
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin

from utils.dependencies.get_user import get_user_db
from models.users import User

SECRET_KEY = os.getenv("SECRET_KEY")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_login(
            self,
            user: User, request: Optional[Request] = None,
            response:  Optional[Response] = None
    ):
        print(f"User {user.id} has logged in.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
