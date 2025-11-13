# -*- coding: utf-8 -*-
from passlib.context import CryptContext
from passlib.hash import bcrypt

__all__ = (
    "verify_password",
    "generate_password_hash",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password: str):
    return bcrypt.hash(password)
