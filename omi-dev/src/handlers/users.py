import random
import typing as t

from pydantic import EmailStr
from fastapi import HTTPException
from dc_core.coreutils.smtp import EMailMessage, send_email
from settings import MAIL_HOST_USER
from datetime import datetime, date

from dc_core.models.db.user import DBUser
from models.requests import (
    GetUserRequest,
    UserStatement,
    UpdateUserRequest,
    ReplenishAccount,
    StatementRequest,
)
from models.responses import (
    GetUserResponse,
    UserResponse,
)

from handlers import BaseHandler

__all__ = ("UsersOmiHandler",)


class UsersOmiHandler(BaseHandler):
    def get_users(self, states: t.Optional[str]) -> t.List[GetUserResponse]:
        rs = self.db_layer.users_omi.get_users_omi(states=states)

        return [GetUserResponse(**r) for r in rs] if rs else []


    def get_user_by_email(
        self, email: EmailStr
    ) -> UserResponse:
        user = self.db_layer.users_omi.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=404, detail=f"Пользователь '{email}' не зарегистрирован в системе"
            )

        return UserResponse(**user)


    def user_statement(self, data: StatementRequest):
        email = data.email
        exists_user = self.db_layer.users_omi.get_user_by_email(email)

        user = self.create_user(email)

        context = {
            "email": email,
        }
        self.add_task(
            send_email,
            EMailMessage(
                to_addrs=[MAIL_HOST_USER],
                subject="Уведомление о регистрация пользователя",
                body=self.templates.get_template("email/notification.txt").render(context),
            ),
        )

        return


    def user_confirm(self, email: EmailStr, current_user: DBUser):
        if 1 not in current_user.role_ids:
            raise HTTPException(403, f"Необходима роль администратора")
        try:
            user = self.get_user_by_email(email)
            if not user:
                raise HTTPException(404, f"Пользователь '{email}' не зарегистрирован в системе")
            elif user.state_id > 0:
                raise HTTPException(404, f"Пользователь '{email}' уже активирован")

            user = self.db_layer.users_omi.user_accept(user=current_user.email, email=email)

            if not user:
                raise HTTPException(404, "Произошла непредвиденная ошибка. Пользователь не изменен")

            self.db_layer.commit()

            self.add_task(
                send_email,
                EMailMessage(
                    to_addrs=[email],
                    subject="Уведомление о завершении регистрации пользователя",
                    body=self.templates.get_template("email/confirm_registration.txt").render(),
                ),
            )
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return


    def user_reject(self, email: EmailStr, current_user: DBUser):
        if 1 not in current_user.role_ids:
            raise HTTPException(403, f"Необходима роль администратора")
        try:
            user = self.get_user_by_email(email)
            if not user:
                raise HTTPException(404, f"Пользователь '{email}' не зарегистрирован в системе")
            elif user.state_id != 0:
                raise HTTPException(404, f"Аккаунт пользователя должен быть на этапе регистрации. Операция отменена")

            user = self.db_layer.users_omi.delete_user_omi(email=email, user=current_user.email)

            if not user:
                raise HTTPException(404, "Произошла непредвиденная ошибка. Операция отменена")

            self.db_layer.commit()

            self.add_task(
                send_email,
                EMailMessage(
                    to_addrs=[email],
                    subject="Уведомление об отклонении заявки на регистрацию пользователя",
                    body=self.templates.get_template("email/reject_registration.txt").render(),
                ),
            )
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return


    def create_user(
        self, email: EmailStr
        #, current_user: DBUser
    ) -> UserResponse:
        # if 1 not in current_user.role_ids:
        #     raise HTTPException(400, f"Для регистрации нового пользователя требуется роль администратора")

        exists_user = self.db_layer.users.get_user_by_email(email)

        if exists_user:
            state_id = exists_user.get("state_id")
            edate = exists_user.get("edate")
            if state_id == 0:
                raise HTTPException(400, f"Пользователь '{email}' уже зарегистрирован в системе. Ожидайте подтверждение регистрации")
            elif state_id > 0 and (edate is None or (edate is not None and edate > date.today())):
                raise HTTPException(400, f"Пользователь '{email}' уже зарегистрирован в системе")
            elif edate <= date.today():
                raise HTTPException(400, f"Срок действия аккаунта пользователя '{email}' истёк. Обратитесь к Администратору")
            else:
                raise HTTPException(400, f"Аккаунт пользователя '{email}' отключен. Обратитесь к Администратору")

        created_user = self.db_layer.users_omi.create_user_omi(
            # user=current_user.email,
            email=email
        )

        if not created_user:
            raise HTTPException(404, "Произошла непредвиденная ошибка. Пользователь не создан")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        # return self.get_user_by_email(email)
        return created_user

    def update_user(self, data: UpdateUserRequest, current_user: DBUser) -> GetUserResponse:
        if 1 not in current_user.role_ids:
            raise HTTPException(403, f"Необходима роль администратора")
        try:
            updated_user = self.db_layer.users_omi.update_user_omi(user=current_user.email, **data.dict())

            if not updated_user:
                raise HTTPException(404, "Произошла непредвиденная ошибка. Пользователь не изменен")

            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return self.get_user_by_email(data.email)

    def delete_user(self, email: str, current_user: DBUser) -> int:
        if 1 not in current_user.role_ids:
            raise HTTPException(403, f"Необходима роль администратора")

        deleted_user = self.db_layer.users_omi.delete_user_omi(email=email, user=current_user.email)

        try:
            if not deleted_user:
                raise HTTPException(404, f"Пользователь '{email}' не зарегистрирован в системе")

            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return deleted_user

    def replenish_account(self, data: ReplenishAccount, current_user: DBUser) -> UserResponse:
        if 1 not in current_user.role_ids:
            raise HTTPException(403, f"Необходима роль администратора")
        try:
            user = self.db_layer.users_omi.replenish_account(user=current_user.email, **data.dict())

            if not user:
                raise HTTPException(404, "Произошла непредвиденная ошибка. Изменения не сохранены")

            self.db_layer.logs.create_log(
                table_name="dir.user",
                record_id=user.get("id"),
                action="replenishment",
                user_id=current_user.id
            )

            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return self.get_user_by_email(data.email)

