"""
Заглушки для моделей ответов dc_core
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class AuthLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


class ChangeEmailResponse(BaseModel):
    success: bool
    message: str


class ChangePasswordResponse(BaseModel):
    success: bool
    message: str


class ConfirmUserResponse(BaseModel):
    success: bool
    message: str


class CreateUserResponse(BaseModel):
    user_id: int
    email: EmailStr
    success: bool


class ForgotPasswordResponse(BaseModel):
    success: bool
    message: str


class PasswordRecoveryResponse(BaseModel):
    success: bool
    message: str


class RefreshAccessTokenResponse(BaseModel):
    access_token: str


class RefreshCodeResponse(BaseModel):
    success: bool
    message: str


class StatementResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None


class AttachmentResponse(BaseModel):
    id: int
    filename: str
    size: int