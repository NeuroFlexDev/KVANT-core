# -*- coding: utf-8 -*-
from typing import List, Optional

from ..models.responses import GetUserResponse

from . import DBLayer

__all__ = ("UserDBLayer",)


class UserDBLayer(DBLayer):
    def get_users(self):
        return self.map_all(self.queries.get_users(self.db))

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.map_one(self.queries.get_user_by_email(self.db, dict(email=email)))

    def get_user_by_id(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.get_user_by_id(self.db, kwargs))

    def get_user_by_guid(self, uuid: str, timeout: Optional[int] = 0) -> Optional[dict]:
        return self.map_one(
            self.queries.get_user_by_guid(self.db, dict(uuid=uuid, timeout=timeout))
        )

    def create_user_omi(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.create_user_omi(self.db, kwargs))

    def create_user(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.create_user(self.db, kwargs))

    def update_user(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.update_user(self.db, kwargs))

    def delete_user(self, email: str) -> Optional[int]:
        return self.queries.delete_user(self.db, dict(email=email))
