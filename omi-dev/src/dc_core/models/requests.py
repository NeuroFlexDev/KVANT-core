"""
Заглушки для моделей запросов dc_core
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChangeEmailRequest(BaseModel):
    new_email: EmailStr
    verification_code: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ConfirmUserRequest(BaseModel):
    email: EmailStr
    verification_code: str


class CreateUserOmiRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class PasswordRecoveryRequest(BaseModel):
    email: EmailStr
    verification_code: str
    new_password: str


class RefreshCodeRequest(BaseModel):
    email: EmailStr


class GetUserRequest(BaseModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None


class CreateStatementRequest(BaseModel):
    title: str
    description: Optional[str] = None


class UpdateStatementRequest(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None