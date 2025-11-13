# -*- coding: utf-8 -*-
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

__all__ = (
    "GetUserResponse",
    "CreateUserResponse",
    "UpdateUserResponse",
)


class GetUserResponse(BaseModel):
    id: int
    state_id: int
    creator: Optional[str]
    createdate: datetime
    modifier: Optional[str]
    modifydate: Optional[datetime]
    email: EmailStr
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    fullname: Optional[str]
    shortname: Optional[str]
    # bdate: Optional[date]
    edate: Optional[date]
    is_admin: bool
    # pw_hash: str = PASSWORD_UNSET
    role_ids: List[int]


class CreateUserResponse(BaseModel):
    uuid: str


class UpdateUserResponse(GetUserResponse):
    pass
