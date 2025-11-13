# -*- coding: utf-8 -*-
from typing import Any, List, Optional

from fastapi.exceptions import HTTPException

from ..coreutils.security import generate_password_hash
from ..coreutils.smtp import EMailMessage, send_email
from ..coreutils.validators import validate_password
from ..models.requests import CreateUserRequest, CreateUserOmiRequest, GetUserRequest, UpdateUserRequest
from ..models.responses import CreateUserResponse, GetUserResponse, UpdateUserResponse

from . import BaseHandler
from settings import MAIL_HOST_USER

__all__ = ("UserHandler",)


class UserHandler(BaseHandler):
    def get_users(self) -> List[GetUserResponse]:
        rs = self.db_layer.users.get_users()
        return [GetUserResponse(**r) for r in rs] if rs else []

    def get_user_by_email(
        self, data: GetUserRequest, current_user: Optional[str] = None
    ) -> GetUserResponse:
        user = self.db_layer.users.get_user_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=404, detail=f"Пользователь '{data.email}' не зарегистрирован в системе"
            )

        return GetUserResponse(**user)

    def create_user(
        self, data: CreateUserRequest, current_user: Optional[str] = None
    ) -> CreateUserResponse:
        if current_user is None:
            raise HTTPException(405, "Регистрация пользователей в систему временно прекращена")

        exists_user = self.db_layer.users.get_user_by_email(data.email)

        if exists_user and exists_user.get("state_id") > 0:
            raise HTTPException(400, f"Пользователь '{data.email}' уже зарегистрирован в системе")

        if not validate_password(data.password):
            raise HTTPException(422, "Пароль не соответствует требованиям безопасности")

        pw_hash = generate_password_hash(data.password)

        created_user = self.db_layer.users.create_user(
            pw_hash=pw_hash, user=current_user, **data.dict()
        )

        if not created_user:
            raise HTTPException(404, "Произошла непредвиденная ошибка. Пользователь не создан")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e
        else:
            context = {
                "activation_keyword": created_user.get("keyword"),
            }
            self.add_task(
                send_email,
                EMailMessage(
                    to_addrs=[created_user.get("email")],
                    subject="Регистрация",
                    body=self.templates.get_template("email/registration.txt").render(context),
                    # body_html=self.templates.get_template("email/registration.html").render(
                    #     context
                    # ),
                ),
            )

        return CreateUserResponse(uuid=created_user.get("guid"))

    def create_user_omi(
        self, data: CreateUserOmiRequest, current_user: Optional[str] = None
    ) -> CreateUserResponse:
        exists_user = self.db_layer.users.get_user_by_email(data.email)

        if exists_user: # and exists_user.get("state_id") > 0:
            raise HTTPException(400, f"Пользователь '{data.email}' уже зарегистрирован в системе")

        if not validate_password(data.password):
            raise HTTPException(422, "Пароль не соответствует требованиям безопасности")

        pw_hash = generate_password_hash(data.password)

        created_user = self.db_layer.users.create_user(
            pw_hash=pw_hash, user=current_user, **data.dict()
        )

        if not created_user:
            raise HTTPException(404, "Произошла непредвиденная ошибка. Пользователь не создан")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e
        else:
            # context = {
            #     "activation_keyword": created_user.get("keyword"),
            # }
            self.add_task(
                send_email,
                EMailMessage(
                    to_addrs=[MAIL_HOST_USER],
                    subject="Уведомление о регистрация пользователя",
                    body=self.templates.get_template("email/notification.txt").render(),
                    # body_html=self.templates.get_template("email/registration.html").render(
                    #     context
                    # ),
                ),
            )

        return CreateUserResponse(uuid=created_user.get("guid"))

    def update_user(self, data: UpdateUserRequest, current_user: str) -> UpdateUserResponse:
        try:
            updated_user = self.db_layer.users.update_user(user=current_user, **data.dict())

            if not updated_user:
                raise HTTPException(404, "Произошла непредвиденная ошибка. Пользователь не изменен")

            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return UpdateUserResponse(**updated_user)

    def delete_user(self, email: str) -> int:
        deleted_user = self.db_layer.users.delete_user(email)

        try:
            if not deleted_user:
                raise HTTPException(404, f"Пользователь '{email}' не зарегистрирован в системе")

            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return deleted_user
