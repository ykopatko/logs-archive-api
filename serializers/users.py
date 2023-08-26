import re

from fastapi_users import schemas
from pydantic import field_validator


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str

    @field_validator("password")
    def validate_password(cls, value: str):
        if len(value) < 8 or len(value) > 30:
            raise ValueError("Password must be between 8 and 30 characters")
        if not re.search("[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search("[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search("[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        return value


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
