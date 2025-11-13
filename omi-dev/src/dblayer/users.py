# -*- coding: utf-8 -*-
from typing import List, Optional

from dc_core.dblayer import DBLayer

__all__ = ("UsersOmiDBLayer",)


class UsersOmiDBLayer(DBLayer):
    def get_users_omi(self, **kwargs):
        return self.map_all(self.queries.get_users_omi(self.db, kwargs))

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.map_one(self.queries.get_user_by_email(self.db, dict(email=email)))

    def get_user_by_guid(self, uuid: str, timeout: Optional[int] = 0) -> Optional[dict]:
        return self.map_one(
            self.queries.get_user_by_guid(self.db, dict(uuid=uuid, timeout=timeout))
        )

    def user_accept(self, **kwargs) -> Optional[int]:
        return self.queries.user_accept(self.db, kwargs)

    def create_user_omi(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.create_user_omi(self.db, kwargs))

    def update_user_omi(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.update_user_omi(self.db, kwargs))

    def delete_user_omi(self, **kwargs) -> Optional[int]:
        return self.queries.delete_user_omi(self.db, kwargs)

    def replenish_account(self, **kwargs):
        return self.map_one(self.queries.replenish_account(self.db, kwargs))
