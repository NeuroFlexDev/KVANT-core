# -*- coding: utf-8 -*-
import os
from typing import Callable, Dict, List, Optional, Union

import aiosql
from aiosql.types import SQLOperationType, SyncDriverAdapterProtocol
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


__all__ = ("DBLayer",)


class SQLAlchemyAdapter(SyncDriverAdapterProtocol):
    def process_sql(self, query_name: str, op_type: SQLOperationType, sql: str) -> str:
        return text(sql)

    def select(
        self,
        db: Session,
        query_name: str,
        sql: str,
        parameters: Union[List, Dict],
        record_class: Optional[Callable],
    ) -> List[Row]:
        return db.execute(sql, parameters).fetchall()

    def select_one(
        self,
        db: Session,
        query_name: str,
        sql: str,
        parameters: Union[List, Dict],
        record_class: Optional[Callable],
    ) -> Optional[Row]:
        return db.execute(sql, parameters).fetchone()

    def insert_update_delete(
        self, db: Session, query_name: str, sql: str, parameters: Union[List, Dict]
    ) -> int:
        return db.execute(sql, parameters)

    def insert_returning(
        self, db: Session, query_name: str, sql: str, parameters: Union[List, Dict]
    ) -> Optional[Row]:
        rs = db.execute(sql, parameters).fetchone()
        return (rs[0] if len(rs) == 1 else rs) if rs else None


class DBLayer:
    def __init__(self, db: Session, sql_path: Optional[str] = None):
        self.db = db
        self.queries = None

        if sql_path:
            self.queries = aiosql.from_path(
                sql_path=sql_path,
                driver_adapter=SQLAlchemyAdapter,
            )

    def commit(self):  # TODO: Remove
        self.db.commit()

    def rollback(self):  # TODO: Remove
        self.db.rollback()

    @staticmethod
    def map_all(rs: List[Row]) -> List[Dict]:
        if not rs:
            return []
        old_row_object = hasattr(rs[0], "keys")

        if old_row_object:
            return [dict(zip(i.keys(), i)) for i in rs]

        return [dict(zip(i._fields, i)) for i in rs]

    @staticmethod
    def map_one(rs: Row) -> Optional[Dict]:
        if not rs:
            return None

        old_row_object = hasattr(rs, "keys")

        if old_row_object:
            return dict(zip(rs.keys(), rs))

        return dict(zip(rs._fields, rs))
