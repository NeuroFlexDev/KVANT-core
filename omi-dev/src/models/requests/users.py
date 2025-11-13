# -*- coding: utf-8 -*-
import typing as t
from datetime import date
from pydantic import BaseModel, EmailStr

__all__ = (
    "GetUserRequest",
    "UpdateUserRequest",
    "UserStatement",
    "ReplenishAccount",
    "StatementRequest",
)


class GetUserRequest(BaseModel):
    email: t.Optional[EmailStr]


class UpdateUserRequest(BaseModel):
    email: EmailStr
    # state_id: t.Optional[int]
    first_name: t.Optional[str]
    middle_name: t.Optional[str]
    last_name: t.Optional[str]
    edate: t.Optional[date] = None
    # is_admin: t.Optional[bool] = False
    role_ids: t.Optional[t.List[int]]
    phone: t.Optional[str]
    organization: t.Optional[str]
    # activity_id: t.Optional[int]
    # calc_number: t.Optional[int]


class UserStatement(BaseModel):
    email: EmailStr


class ReplenishAccount(BaseModel):
    email: EmailStr
    value: int


class StatementRequest(BaseModel):
    email: EmailStr
