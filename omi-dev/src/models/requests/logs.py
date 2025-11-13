# -*- coding: utf-8 -*-
import typing as t
from pydantic import BaseModel, EmailStr
from datetime import date

__all__ = (
    "CreateLogRequest",
)


class CreateLogRequest(BaseModel):
    table_name: str
    record_id: int
    action: str
