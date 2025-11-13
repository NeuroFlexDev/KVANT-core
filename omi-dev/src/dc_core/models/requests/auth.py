# -*- coding: utf-8 -*-
from pydantic import BaseModel, EmailStr

__all__ = (
    "AuthLoginRequest",
    "ConfirmUserRequest",
    "ChangePasswordRequest",
    "ChangeEmailRequest",
    "ForgotPasswordRequest",
    "PasswordRecoveryRequest",
    "RefreshCodeRequest",
)


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


class ConfirmUserRequest(BaseModel):
    uuid: str
    keyword: str


class ChangePasswordRequest(BaseModel):
    password_old: str
    password_new: str


class ChangeEmailRequest(BaseModel):
    email_new: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class PasswordRecoveryRequest(BaseModel):
    uuid: str
    password_new: str
    keyword: str


class RefreshCodeRequest(BaseModel):
    uuid: str
