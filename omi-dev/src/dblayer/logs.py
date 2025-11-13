# -*- coding: utf-8 -*-
from dc_core.dblayer import DBLayer

__all__ = ("LogsDBLayer",)


class LogsDBLayer(DBLayer):
    def get_logs(self, **kwargs):
        return self.map_all(self.queries.get_logs(self.db, kwargs))

    def create_log(self, **kwargs):
        return self.map_one(self.queries.create_log(self.db, kwargs))
