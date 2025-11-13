# -*- coding: utf-8 -*-
from fastapi import APIRouter, BackgroundTasks, Depends
from utils.depends import get_current_user, get_db, get_settings
from handlers.users import UsersOmiHandler
from handlers.auth import AuthHandler
from handlers.users import UsersOmiHandler as UserHandler
from models.requests import UserStatement, StatementRequest
from pydantic import EmailStr
from dc_core.models.requests import (
    AuthLoginRequest,
    ChangeEmailRequest,
    ChangePasswordRequest,
    ConfirmUserRequest,
    CreateUserOmiRequest,
    ForgotPasswordRequest,
    PasswordRecoveryRequest,
    RefreshCodeRequest,
    GetUserRequest
)

from dc_core.models.responses import (
    AuthLoginResponse,
    ChangeEmailResponse,
    ChangePasswordResponse,
    ConfirmUserResponse,
    CreateUserResponse,
    ForgotPasswordResponse,
    PasswordRecoveryResponse,
    RefreshAccessTokenResponse,
    RefreshCodeResponse,
)
from settings import SENTRY_ENV, SENTRY_DSN

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthLoginResponse)
async def login(data: AuthLoginRequest, db=Depends(get_db), settings=Depends(get_settings)):
    return AuthHandler(db, settings=settings).login(data)


@router.post("/refresh_token", response_model=RefreshAccessTokenResponse)
async def refresh(refresh_token: str, db=Depends(get_db), settings=Depends(get_settings)):
    return AuthHandler(db, settings=settings).refresh_token(refresh_token)


@router.post("/statement")
async def registration(data: StatementRequest,
                       bt: BackgroundTasks,
                       db=Depends(get_db),
                       settings=Depends(get_settings)
                       ):
    return UsersOmiHandler(db, settings=settings, background_tasks=bt).user_statement(data)


# @router.post("/registration", response_model=CreateUserResponse)
# async def registration(data: CreateUserOmiRequest, bt: BackgroundTasks, db=Depends(get_db),
#                        settings=Depends(get_settings)):
#     return UserHandler(db, settings=settings, background_tasks=bt).create_user_omi(data)


@router.put("/registration/confirm")
async def user_confirm(email: EmailStr,
                      bt: BackgroundTasks,
                      db=Depends(get_db),
                      current_user=Depends(get_current_user),
                      settings=Depends(get_settings)
                      ):
    return UsersOmiHandler(db, settings=settings, background_tasks=bt).user_confirm(email, current_user)


@router.put("/registration/reject")
async def user_reject(email: EmailStr,
                       bt: BackgroundTasks,
                       db=Depends(get_db),
                       current_user=Depends(get_current_user),
                       settings=Depends(get_settings)
                       ):
    return UsersOmiHandler(db, settings=settings, background_tasks=bt).user_reject(email, current_user)


@router.put("/confirm_user", response_model=ConfirmUserResponse)
async def confirmation(data: ConfirmUserRequest, db=Depends(get_db), settings=Depends(get_settings)):
    return AuthHandler(db, settings=settings).confirm_user(data)


@router.put("/forgot_password", response_model=ForgotPasswordResponse)
async def forgot_password(data: ForgotPasswordRequest, bt: BackgroundTasks, db=Depends(get_db),
                          settings=Depends(get_settings)):
    return AuthHandler(db, settings=settings, background_tasks=bt).forgot_password(data)


@router.put("/password_recovery", response_model=PasswordRecoveryResponse)
async def password_recovery(data: PasswordRecoveryRequest, db=Depends(get_db), settings=Depends(get_settings)):
    return AuthHandler(db, settings=settings).password_recovery(data)


@router.put("/change_password", response_model=ChangePasswordResponse)
async def change_password(
    data: ChangePasswordRequest, db=Depends(get_db), current_user=Depends(get_current_user),
        settings=Depends(get_settings)
):
    return AuthHandler(db, settings=settings).change_password(data, current_user)


@router.put("/change_email", response_model=ChangeEmailResponse)
async def change_email(
    data: ChangeEmailRequest,
    bt: BackgroundTasks,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
    settings=Depends(get_settings)
):
    return AuthHandler(db, settings=settings, background_tasks=bt).change_email(data, current_user)


@router.put("/refresh_code", response_model=RefreshCodeResponse)
async def refresh_code(data: RefreshCodeRequest, bt: BackgroundTasks, db=Depends(get_db),
                       settings=Depends(get_settings)):
    return AuthHandler(db, settings=settings, background_tasks=bt).refresh_code(data)
