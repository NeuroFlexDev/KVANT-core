# -*- coding: utf-8 -*-
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

__all__ = ("DBUser",)

PASSWORD_UNSET = "<unset>"


class DBUser(BaseModel):
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
    edate: Optional[date]
    is_admin: bool
    pw_hash: str = PASSWORD_UNSET
    keyword: Optional[str]
    guid: str
    email_new: Optional[EmailStr]
    role_ids: list
