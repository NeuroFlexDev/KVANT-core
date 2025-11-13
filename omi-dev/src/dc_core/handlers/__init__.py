# -*- coding: utf-8 -*-
import logging
import os
import typing

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..dblayer.factory import DBLayerFactory

__all__ = ("BaseHandler",)


class BaseHandler:
    def __init__(self, db: Session, settings: typing.Dict = None, background_tasks=None, dblayer=None):
        self.settings = self._load_settings(settings)
        self.db_layer = dblayer if dblayer else DBLayerFactory(db)
        self.back_tasks = background_tasks
        if hasattr(self.settings, "TEMPLATES_FOLDER"):
            self.templates = Jinja2Templates(directory=self.settings.TEMPLATES_FOLDER)
        else:
            self.templates = None
            logging.warning("No template folder attached")

    def add_task(self, *args, **kwargs):
        if not self.back_tasks:
            logging.error("No background tasks attached")
            return

        self.back_tasks.add_task(*args, **kwargs)

    def _load_settings(self, settings: typing.Dict = None):
        class _GlobalSettings:
            pass

        if settings:
            for key, value in settings.items():
                setattr(_GlobalSettings, key, value)

        return _GlobalSettings()
