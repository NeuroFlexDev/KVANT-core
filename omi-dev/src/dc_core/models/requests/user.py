# -*- coding: utf-8 -*-
from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr

__all__ = (
    "GetUserRequest",
    "CreateUserOmiRequest",
    "CreateUserRequest",
    "UpdateUserRequest",
)


class GetUserRequest(BaseModel):
    email: Optional[EmailStr]


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]


class CreateUserOmiRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    organization: Optional[str]
    activity_id: Optional[int]


class UpdateUserRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    edate: Optional[date] = None
    is_admin: Optional[bool] = False
    role_ids: Optional[List[int]]
