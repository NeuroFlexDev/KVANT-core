# -*- coding: utf-8 -*-
import typing as t
from datetime import date, datetime
from pydantic import BaseModel, EmailStr

__all__ = (
    "GetUserResponse",
    "UserResponse",
)

class GetUserResponse(BaseModel):
    id: int
    state_id: int
    state_name: str
    creator: t.Optional[str]
    createdate: datetime
    modifier: t.Optional[str]
    modifydate: t.Optional[datetime]
    email: EmailStr
    first_name: t.Optional[str]
    middle_name: t.Optional[str]
    last_name: t.Optional[str]
    fullname: t.Optional[str]
    shortname: t.Optional[str]
    # bdate: t.Optional[date]
    edate: t.Optional[date]
    # is_admin: bool
    # pw_hash: str = PASSWORD_UNSET
    role_ids: t.List[int]
    phone: t.Optional[str]
    organization: t.Optional[str]
    activity_id: t.Optional[int]
    calc_number: t.Optional[int]

class UserResponse(GetUserResponse):
    calc_number: t.Optional[int]
