# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from settings import (
    DB_ECHO,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_SSLMODE,
    DB_SSLROOTCERT,
    DB_USER,
)

__all__ = ("Session",)


params = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "port": DB_PORT,
    "dbname": DB_NAME
}

if DB_SSLMODE:
    params.setdefault("sslmode", DB_SSLMODE)

if DB_SSLROOTCERT:
    params.setdefault("sslrootcert", DB_SSLROOTCERT)

engine = create_engine(
    "postgresql+psycopg2://", connect_args=params, poolclass=QueuePool, echo=DB_ECHO
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)
