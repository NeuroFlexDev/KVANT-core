from typing import Optional, List
from . import DBLayer

__all__ = ("StorageDBLayer",)


class StorageDBLayer(DBLayer):
    def get_statements(self, **kwargs) -> List[dict]:
        return self.map_all(self.queries.get_statements(self.db, kwargs))

    def get_statement_by_id(self, **kwargs) -> Optional[dict]:
        return self.map_all(self.queries.get_statement_by_id(self.db, kwargs))

    def get_statement_by_guid(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.get_statement_by_guid(self.db, kwargs))

    def create_statement(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.create_statement(self.db, kwargs))

    def update_statement(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.update_statement(self.db, kwargs))

    def delete_statement(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.delete_statement(self.db, kwargs))

    def create_attachment(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.create_attachment(self.db, kwargs))

    def get_attachments_by_statement_guid(self, **kwargs) -> List[dict]:
        return self.map_all(self.queries.get_attachments_by_statement_guid(self.db, kwargs))

    def get_attachment_by_guid(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.get_attachment_by_guid(self.db, kwargs))

    def delete_attachment(self, **kwargs) -> Optional[dict]:
        return self.map_one(self.queries.delete_attachment(self.db, kwargs))
