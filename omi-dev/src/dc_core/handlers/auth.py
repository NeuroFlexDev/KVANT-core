# -*- coding: utf-8 -*-
import datetime

from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from ..coreutils.jwt import create_access_token, create_refresh_token, get_payload_from_token
from ..coreutils.security import generate_password_hash, verify_password
from ..coreutils.smtp import EMailMessage, send_email
from ..coreutils.validators import validate_password
from ..models.db.user import DBUser
from ..models.requests import (
    AuthLoginRequest,
    ChangeEmailRequest,
    ChangePasswordRequest,
    ConfirmUserRequest,
    ForgotPasswordRequest,
    PasswordRecoveryRequest,
    RefreshCodeRequest,
)
from ..models.responses import (
    AuthLoginResponse,
    ChangeEmailResponse,
    ChangePasswordResponse,
    ConfirmUserResponse,
    ForgotPasswordResponse,
    PasswordRecoveryResponse,
    RefreshAccessTokenResponse,
    RefreshCodeResponse,
)

from . import BaseHandler

__all__ = ("AuthHandler",)


class AuthHandler(BaseHandler):
    def login(self, data: AuthLoginRequest, **kwargs) -> AuthLoginResponse:
        user = self.db_layer.auth.get_user_for_auth(data.email)

        if not user:
            raise HTTPException(404, f"Пользователь '{data.email}' не зарегистрирован в системе")

        if not verify_password(data.password, user.get("pw_hash")):
            raise HTTPException(400, "Неверное имя пользователя или пароль")

        access_token, expired = create_access_token(
            user.get("id"), data.email, user.get("pw_hash"), self.settings.SECRET_KEY
        )
        refresh_token = create_refresh_token(
            user.get("id"), data.email, user.get("pw_hash"), self.settings.SECRET_KEY
        )

        return AuthLoginResponse(access=access_token, refresh=refresh_token, exp=expired)

    def refresh_token(self, refresh_token: str) -> RefreshAccessTokenResponse:
        no_credentials = HTTPException(HTTP_403_FORBIDDEN, "Неверный токен")

        try:
            jwt_payload = get_payload_from_token(refresh_token, self.settings.SECRET_KEY)
        except Exception as e:
            raise no_credentials

        user = self.db_layer.auth.get_user_for_auth(jwt_payload.email, jwt_payload.pw_hash)

        if not user:
            raise no_credentials

        access_token, expired = create_access_token(
            user.get("id"), user.get("email"), user.get("pw_hash"), self.settings.SECRET_KEY
        )

        return RefreshAccessTokenResponse(access=access_token, exp=expired)

    def confirm_user(self, data: ConfirmUserRequest) -> ConfirmUserResponse:
        exists_user = self.db_layer.users.get_user_by_guid(uuid=data.uuid, timeout=self.settings.CONFIRM_TIMEOUT)

        if not exists_user:
            raise HTTPException(404, "Пользователь не зарегистрирован в системе")

        if exists_user.get("is_expired"):
            raise HTTPException(422, "Истек срок подтверждения операции")

        confirmed_user = self.db_layer.auth.confirm_user(pw_hash_new=None, **data.dict())

        if not confirmed_user:
            raise HTTPException(400, "Неверный код")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return ConfirmUserResponse()

    def forgot_password(self, data: ForgotPasswordRequest) -> ForgotPasswordResponse:
        forgot_user = self.db_layer.auth.forgot_password(user=data.email)

        if not forgot_user:
            raise HTTPException(404, f"Пользователь '{data.email}' не зарегистрирован в системе")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e
        else:
            context = {
                "recovery_email": forgot_user.get("email"),
                "recovery_keyword": forgot_user.get("keyword"),
            }
            self.add_task(
                send_email,
                EMailMessage(
                    to_addrs=[forgot_user.get("email")],
                    subject="Восстановление пароля",
                    body=self.templates.get_template("email/password_recovery.txt").render(context),
                    # body_html=self.templates.get_template("email/password_recovery.html").render(
                    #     context
                    # ),
                ),
            )

        return ForgotPasswordResponse(uuid=forgot_user.get("guid"))

    def password_recovery(self, data: PasswordRecoveryRequest) -> PasswordRecoveryResponse:
        exists_user = self.db_layer.users.get_user_by_guid(uuid=data.uuid, timeout=self.settings.CONFIRM_TIMEOUT)

        if not exists_user:
            raise HTTPException(404, "Пользователь не зарегистрирован в системе")

        if exists_user.get("is_expired"):
            raise HTTPException(422, "Истек срок выполнения операции")

        if validate_password(data.password_new):
            pw_hash_new = generate_password_hash(data.password_new)
        else:
            raise HTTPException(422, "Новый пароль не соответствует требованиям безопасности")

        recovery_user = self.db_layer.auth.confirm_user(pw_hash_new=pw_hash_new, **data.dict())

        if not recovery_user:
            raise HTTPException(404, "Неверный код")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return PasswordRecoveryResponse()

    def change_password(
        self, data: ChangePasswordRequest, current_user: DBUser
    ) -> ChangePasswordResponse:
        if verify_password(data.password_new, current_user.pw_hash):
            raise HTTPException(422, "Новый пароль должен отличаться от старого")

        if not verify_password(data.password_old, current_user.pw_hash):
            raise HTTPException(422, "Неверный пароль")

        if validate_password(data.password_new):
            pw_hash_new = generate_password_hash(data.password_new)
        else:
            raise HTTPException(422, "Новый пароль не соответствует требованиям безопасности")

        self.db_layer.auth.change_password(user=current_user.email, pw_hash_new=pw_hash_new)

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return ChangePasswordResponse()

    def change_email(self, data: ChangeEmailRequest, current_user: DBUser) -> ChangeEmailResponse:
        if data.email_new == current_user.email:
            raise HTTPException(422, "Старый и новый email не должны совпадать")

        exists_user = self.db_layer.users.get_user_by_email(data.email_new)

        if exists_user:
            raise HTTPException(400, "Email привязан к другой учетной записи")

        changed_user = self.db_layer.auth.change_email(user=current_user.email, **data.dict())
        if not changed_user:
            raise HTTPException(404, "Пользователь не зарегистрирован в системе")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e
        else:
            context = {
                "change_email": changed_user.get("email_new"),
                "change_keyword": changed_user.get("keyword"),
            }
            self.add_task(
                send_email,
                EMailMessage(
                    to_addrs=[changed_user.get("email_new")],
                    subject="Изменение адреса электронной почты",
                    body=self.templates.get_template("email/change_email.txt").render(context),
                    # body_html=self.templates.get_template("email/change_email.html").render(
                    #     context
                    # ),
                ),
            )

        return ChangeEmailResponse(uuid=changed_user.get("guid"))

    def refresh_code(self, data: RefreshCodeRequest) -> RefreshCodeResponse:
        exists_user = self.db_layer.users.get_user_by_guid(data.uuid, timeout=self.settings.CONFIRM_TIMEOUT)

        if not exists_user:
            raise HTTPException(404, "Пользователь не зарегистрирован в системе")

        if exists_user.get("state_id") == 1 or exists_user.get("keyword") == None:
            raise HTTPException(404, "Пользователь не совершал операций, требующих обновление кода")

        changed_user = self.db_layer.auth.refresh_code(**data.dict())

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e
        else:
            if changed_user.get("state_id") == 0:
                context = {
                    "activation_keyword": changed_user.get("keyword"),
                }
                self.add_task(
                    send_email,
                    EMailMessage(
                        to_addrs=[changed_user.get("email")],
                        subject="Регистрация",
                        body=self.templates.get_template("email/registration.txt").render(context),
                        # body_html=self.templates.get_template("email/registration.html").render(
                        #     context
                        # ),
                    ),
                )
            elif changed_user.get("state_id") == 2:
                context = {
                    "change_email": changed_user.get("email_new"),
                    "change_keyword": changed_user.get("keyword"),
                }
                self.add_task(
                    send_email,
                    EMailMessage(
                        to_addrs=[changed_user.get("email_new")],
                        subject="Изменение адреса электронной почты",
                        body=self.templates.get_template("email/change_email.txt").render(context),
                        # body_html=self.templates.get_template("email/change_email.html").render(
                        #     context
                        # ),
                    ),
                )
            elif changed_user.get("state_id") == 3:
                context = {
                    "recovery_email": changed_user.get("email"),
                    "recovery_keyword": changed_user.get("keyword"),
                }
                self.add_task(
                    send_email,
                    EMailMessage(
                        to_addrs=[changed_user.get("email")],
                        subject="Восстановление пароля",
                        body=self.templates.get_template("email/password_recovery.txt").render(
                            context
                        ),
                        # body_html=self.templates.get_template(
                        #     "email/password_recovery.html"
                        # ).render(context),
                    ),
                )
            else:
                raise HTTPException(404, "Unknown operation code")
        return RefreshCodeResponse()
