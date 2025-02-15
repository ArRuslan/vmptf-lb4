from time import time

import bcrypt
from fastapi import APIRouter

from .. import config
from ..models import User, Session
from ..schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from ..utils.multiple_errors_exception import MultipleErrorsException

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest):
    if await User.filter(email=data.email).exists():
        raise MultipleErrorsException("User with this email already registered!")

    password = bcrypt.hashpw(data.password.encode("utf8"), bcrypt.gensalt(config.BCRYPT_ROUNDS)).decode("utf8")
    user = await User.create(
        email=data.email,
        password=password,
        first_name=data.first_name,
        last_name=data.last_name,
    )
    session = await Session.create(user=user)

    return {
        "token": session.to_jwt(),
        "expires_at": int(time() + config.AUTH_JWT_TTL),
    }


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    if (user := await User.get_or_none(email=data.email)) is None:
        raise MultipleErrorsException("User with this credentials is not found!")

    if not bcrypt.checkpw(data.password.encode("utf8"), user.password.encode("utf8")):
        raise MultipleErrorsException("User with this credentials is not found!")

    session = await Session.create(user=user)

    return {
        "token": session.to_jwt(),
        "expires_at": int(time() + config.AUTH_JWT_TTL),
    }
