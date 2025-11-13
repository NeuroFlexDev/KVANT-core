# -*- coding: utf-8 -*-
from dc_core.dblayer.factory import DBLayerFactory as BasicDBLayerFactory
from os.path import dirname, join
from sqlalchemy.orm import Session

from .directories import DirectoriesDBLayer
from .registries import RegistriesDBLayer
from .logs import LogsDBLayer
from .users import UsersOmiDBLayer
from .questionnaire import QuestionnaireDBLayer


__all__ = ("DBLayerFactory",)


class DBLayerFactory(BasicDBLayerFactory):
    def __init__(self, db: Session, *args, **kwargs):
        super().__init__(db=db, *args, **kwargs)
        self.directories = DirectoriesDBLayer(db=db, sql_path=join(dirname(__file__), "sql", "directories"))
        self.registries = RegistriesDBLayer(db=db, sql_path=join(dirname(__file__), "sql", "registries"))
        self.logs = LogsDBLayer(db=db, sql_path=join(dirname(__file__), "sql", "logs"))
        self.users_omi = UsersOmiDBLayer(db=db, sql_path=join(dirname(__file__), "sql", "users"))
        self.questionnaire = QuestionnaireDBLayer(db=db, sql_path=join(dirname(__file__), "sql", "questionnaire"))
