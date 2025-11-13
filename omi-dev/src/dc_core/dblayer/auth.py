# -*- coding: utf-8 -*-
from typing import Optional

from . import DBLayer

__all__ = ("AuthDBLayer",)


class AuthDBLayer(DBLayer):
    def get_user_for_auth(self, email: str, pw_hash: str = None) -> Optional[dict]:
        return self.map_one(
            self.queries.get_user_for_auth(self.db, dict(email=email, pw_hash=pw_hash))
        )

    def confirm_user(self, **kwargs) -> Optional[str]:
        return self.queries.confirm_user(self.db, kwargs)

    def change_password(self, **kwargs):
        return self.queries.change_password(self.db, kwargs)

    def change_email(self, **kwargs):
        return self.map_one(self.queries.change_email(self.db, kwargs))

    def forgot_password(self, **kwargs):
        return self.map_one(self.queries.forgot_password(self.db, kwargs))

    def password_recovery(self, **kwargs):
        return self.map_one(self.queries.password_recovery(self.db, kwargs))

    def refresh_code(self, **kwargs):
        return self.map_one(self.queries.refresh_code(self.db, kwargs))
