# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional

from dc_core.handlers.auth import AuthHandler as CoreAuthHandler
from dc_core.models.requests import (
    AuthLoginRequest,
    ChangeEmailRequest,
    ChangePasswordRequest,
    ConfirmUserRequest,
    ForgotPasswordRequest,
    PasswordRecoveryRequest,
    RefreshCodeRequest,
)
from dc_core.models.responses import (
    AuthLoginResponse,
    ChangeEmailResponse,
    ChangePasswordResponse,
    ConfirmUserResponse,
    ForgotPasswordResponse,
    PasswordRecoveryResponse,
    RefreshAccessTokenResponse,
    RefreshCodeResponse,
)

from handlers import BaseHandler

__all__ = ("AuthHandler",)


class AuthHandler(BaseHandler):
    """Обёртка над базовой реализацией аутентификации из dc_core."""

    def __init__(self, *args, **kwargs):
        self._raw_db = kwargs.get("db") if "db" in kwargs else (args[0] if args else None)
        self._settings: Optional[Dict[str, Any]] = kwargs.get("settings")
        self._background_tasks = kwargs.get("background_tasks")

        super().__init__(*args, **kwargs)

        if self._raw_db is None:
            raise ValueError("Database session is required for AuthHandler")

        self._core = CoreAuthHandler(
            db=self._raw_db,
            settings=self._settings,
            background_tasks=self._background_tasks,
            dblayer=self.dblayer,
        )

    def login(self, data: AuthLoginRequest) -> AuthLoginResponse:
        return self._core.login(data)

    def refresh_token(self, refresh_token: str) -> RefreshAccessTokenResponse:
        return self._core.refresh_token(refresh_token)

    def confirm_user(self, data: ConfirmUserRequest) -> ConfirmUserResponse:
        return self._core.confirm_user(data)

    def forgot_password(self, data: ForgotPasswordRequest) -> ForgotPasswordResponse:
        return self._core.forgot_password(data)

    def password_recovery(self, data: PasswordRecoveryRequest) -> PasswordRecoveryResponse:
        return self._core.password_recovery(data)

    def change_password(
        self, data: ChangePasswordRequest, current_user
    ) -> ChangePasswordResponse:
        return self._core.change_password(data, current_user)

    def change_email(
        self, data: ChangeEmailRequest, current_user
    ) -> ChangeEmailResponse:
        return self._core.change_email(data, current_user)

    def refresh_code(self, data: RefreshCodeRequest) -> RefreshCodeResponse:
        return self._core.refresh_code(data)
