import typing

from dblayer.factory import DBLayerFactory


__all__ = ("BaseHandler",)


class BaseHandler:
    """Базовый класс для всех handlers"""
    def __init__(self, *args, **kwargs):
        kwargs.pop("dblayer", None)
        self.dblayer = DBLayerFactory(*args, **kwargs)
        # Provide backward compatible attribute name
        self.db_layer = self.dblayer

    def get_db(self):
        return self.dblayer
