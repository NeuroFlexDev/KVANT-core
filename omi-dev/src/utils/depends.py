# -*- coding: utf-8 -*-
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from handlers.auth import AuthHandler
from dc_core.models.db.user import DBUser
from settings import SECRET_KEY

from dc_core.coreutils.jwt import get_payload_from_token

__all__ = (
    "get_db",
    "get_current_user",
    "get_settings",
)


token_header = APIKeyHeader(name="X-Auth-Token", auto_error=False)
token_query = APIKeyQuery(name="token", auto_error=False)


def get_db(request: Request):
    return request.state.db


def get_settings(request: Request):
    return request.state.settings


def get_current_user(
    token_h: str = Security(token_header), token_q: str = Security(token_query), db=Depends(get_db)
) -> DBUser:
    if token_h:
        token = token_h
    elif token_q:
        token = token_q
    else:
        raise HTTPException(HTTP_403_FORBIDDEN, "Could not validate credentials (no token)")

    no_credentials = HTTPException(HTTP_403_FORBIDDEN, "Could not validate credentials")

    try:
        jwt_payload = get_payload_from_token(token, SECRET_KEY)
    except Exception as e:
        raise no_credentials from e

    if not jwt_payload:
        raise no_credentials

    user = AuthHandler(db).db_layer.auth.get_user_for_auth(jwt_payload.email, jwt_payload.pw_hash)
    if not user:
        raise no_credentials

    return DBUser(**user)
