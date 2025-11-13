# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Tuple

import os
import jwt
import pendulum
from pydantic import BaseModel, ValidationError


ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", default=60 * 48)  # 48 часов
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", default=60 * 24 * 30)  # 1 месяц
TOKEN_ALGORITHM = "HS256"


__all__ = (
    "create_access_token",
    "create_refresh_token",
    "get_payload_from_token",
)


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTPayload(BaseModel):
    id: int
    email: str
    pw_hash: str


def create_jwt_token(
    *, jwt_content: JWTPayload, secret_key: str, expires_delta: timedelta
) -> Tuple[str, datetime]:
    to_encode = jwt_content.dict().copy()
    expire = pendulum.now() + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub="access"))
    return jwt.encode(to_encode, secret_key, TOKEN_ALGORITHM), expire


def create_access_token(
    user_id: int, email: str, pw_hash: str, secret_key: str
) -> Tuple[str, datetime]:
    return create_jwt_token(
        jwt_content=_get_token_payload(user_id, email, pw_hash),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: int, email: str, pw_hash: str, secret_key: str) -> str:
    token, _ = create_jwt_token(
        jwt_content=_get_token_payload(user_id, email, pw_hash),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    return token


def get_payload_from_token(token: str, secret_key: str) -> JWTPayload:
    try:
        return JWTPayload(**jwt.decode(token, secret_key, algorithms=[TOKEN_ALGORITHM]))
    except jwt.PyJWTError as e:
        raise ValueError("Unable to decode JWT token") from e
    except ValidationError as e:
        raise ValueError("Malformed payload in token") from e


def _get_token_payload(user_id: int, email: str, pw_hash: str) -> JWTPayload:
    return JWTPayload(id=user_id, email=email, pw_hash=pw_hash)
