# -*- coding: utf-8 -*-
from os.path import dirname, join
from sqlalchemy.orm import Session

from .auth import *
from .users import *
from .storage import *

__all__ = ("DBLayerFactory",)


class DBLayerFactory:
    def __init__(self, db: Session, *args, **kwargs):
        self._db = db
        _dir = join(dirname(__file__), "sql")
        self.users = UserDBLayer(db=db, sql_path=join(_dir, "users"))
        self.auth = AuthDBLayer(db=db, sql_path=join(_dir, "auth"))
        self.storage = StorageDBLayer(db=db, sql_path=join(_dir, "storage"))

    def commit(self):
        self._db.commit()

    def rollback(self):
        self._db.rollback()
