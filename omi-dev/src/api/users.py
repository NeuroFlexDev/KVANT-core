# -*- coding: utf-8 -*-
import typing as t
from fastapi import APIRouter, Depends
from pydantic import EmailStr

from utils.depends import get_current_user, get_db
from handlers.users import UsersOmiHandler
from handlers.users import UsersOmiHandler as UserHandler
from dc_core.models.requests import CreateUserOmiRequest
from dc_core.models.responses import CreateUserResponse
from models.requests import (
    GetUserRequest,
    UpdateUserRequest,
    ReplenishAccount,
)
from models.responses import (
    # CreateUserResponse,
    GetUserResponse,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=t.List[GetUserResponse])
async def get_users(states: t.Optional[str] = '0,1,2,3', db=Depends(get_db), current_user=Depends(get_current_user)):
    return UsersOmiHandler(db).get_users(states)


# @router.get("/{id}", response_model=UserOmiResponse)
# async def get_user_by_id(
#     id: int, db=Depends(get_db), current_user=Depends(get_current_user)
# ):
#     return UserHandler(db).get_user_by_id(id, current_user)


@router.get("/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str, db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    return UsersOmiHandler(db).get_user_by_email(email)


# @router.post("/", response_model=UserResponse)
# async def create_user(
#     email: EmailStr,
#     db=Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     return UsersOmiHandler(db).create_user(email, current_user)


@router.put("/replenish_account", response_model=UserResponse)
async def replenish_account(
    data: ReplenishAccount, db=Depends(get_db), current_user=Depends(get_current_user)
):
    return UsersOmiHandler(db).replenish_account(data, current_user)


@router.put("/{email}", response_model=GetUserResponse)
async def update_user(
    data: UpdateUserRequest, db=Depends(get_db), current_user=Depends(get_current_user)
):
    return UsersOmiHandler(db).update_user(data, current_user)


@router.delete("/{email}")
async def delete_user(email: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    return UsersOmiHandler(db).delete_user(email, current_user)
