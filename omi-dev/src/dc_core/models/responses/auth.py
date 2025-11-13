# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel

__all__ = (
    "AuthLoginResponse",
    "ConfirmUserResponse",
    "ChangePasswordResponse",
    "ChangeEmailResponse",
    "ForgotPasswordResponse",
    "PasswordRecoveryResponse",
    "RefreshAccessTokenResponse",
    "RefreshCodeResponse",
)


class RefreshAccessTokenResponse(BaseModel):
    access: str
    exp: datetime


class AuthLoginResponse(RefreshAccessTokenResponse):
    refresh: str


class ConfirmUserResponse(BaseModel):
    pass


class ChangePasswordResponse(BaseModel):
    pass


class ChangeEmailResponse(BaseModel):
    uuid: str


class ForgotPasswordResponse(BaseModel):
    uuid: str


class PasswordRecoveryResponse(BaseModel):
    pass


class RefreshCodeResponse(BaseModel):
    pass
