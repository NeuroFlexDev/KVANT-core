# -*- coding: utf-8 -*-
import logging
from importlib import import_module
from typing import List

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sentry_asgi import SentryMiddleware

from utils.db import Session
from settings import API_ROUTES, APP_TITLE, SENTRY_DSN

logger = logging.getLogger(__name__)
app = FastAPI(title=APP_TITLE, docs_url="/api/docs", openapi_url="/api/openapi.json")
origins = [
    "https://kvant.id",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SentryMiddleware)


def api_routes(apis: List[str]) -> APIRouter:
    _api_router = APIRouter(prefix="/api")

    for name in apis:
        m = import_module(f"api.{name}")

        for item in dir(m):
            item = getattr(m, item)

            if isinstance(item, APIRouter):
                _api_router.include_router(item)

    return _api_router


app.include_router(api_routes(API_ROUTES))


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        request.state.db = Session()
        response = await call_next(request)
    except Exception as e:
        logger.exception(e)
    finally:
        request.state.db.close()

    return response


@app.middleware("http")
async def global_settings_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        im = import_module("settings")
        request.state.settings = {k: getattr(im, k) for k in dir(im)}
        response = await call_next(request)
    except Exception as e:
        logger.exception(e)

    return response


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logger.exception(exc)
    return JSONResponse(str(exc), status_code=HTTP_500_INTERNAL_SERVER_ERROR)
