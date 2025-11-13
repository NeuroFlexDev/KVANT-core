# -*- coding: utf-8 -*-
from pydantic import BaseModel
from datetime import datetime

__all__ = (
    "LogResponse",
)


class LogResponse(BaseModel):
    id: int
    creator_id: int
    createdate: datetime
    table_name: str
    record_id: int
    action: str
