import typing as t
from datetime import date
from models.responses import (
    LogResponse
)

from handlers import BaseHandler

__all__ = ("LogsHandler",)


class LogsHandler(BaseHandler):
    def get_logs(self, user_id, table_name, record_id, date_from, date_to, action) -> t.List[LogResponse]:
        rs = self.db_layer.logs.get_logs(
            user_id=user_id,
            table_name=table_name,
            record_id=record_id,
            date_from=date_from,
            date_to=date_to,
            action=action
        )
        return [LogResponse(**r) for r in rs] if rs else []
