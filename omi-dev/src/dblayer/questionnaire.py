# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional

from dc_core.dblayer import DBLayer

__all__ = ("QuestionnaireDBLayer",)


class QuestionnaireDBLayer(DBLayer):
    def list_forms(self, **kwargs) -> List[Dict[str, Any]]:
        return self.map_all(self.queries.list_forms(self.db, kwargs))

    def get_form_by_id(self, **kwargs) -> Optional[Dict[str, Any]]:
        return self.map_one(self.queries.get_form_by_id(self.db, kwargs))

    def get_form_with_sections(self, **kwargs) -> Optional[Dict[str, Any]]:
        return self.map_one(self.queries.get_form_with_sections(self.db, kwargs))

    def create_form(self, **kwargs) -> Dict[str, Any]:
        return self.map_one(self.queries.create_form(self.db, kwargs))

    def update_form(self, **kwargs) -> Optional[Dict[str, Any]]:
        return self.map_one(self.queries.update_form(self.db, kwargs))

    def mark_form_deleted(self, **kwargs) -> Optional[Dict[str, Any]]:
        return self.map_one(self.queries.mark_form_deleted(self.db, kwargs))

    def list_sections(self, **kwargs) -> List[Dict[str, Any]]:
        return self.map_all(self.queries.list_sections(self.db, kwargs))

    def get_section(self, **kwargs) -> Optional[Dict[str, Any]]:
        return self.map_one(self.queries.get_section(self.db, kwargs))

    def upsert_section(self, **kwargs) -> Dict[str, Any]:
        return self.map_one(self.queries.upsert_section(self.db, kwargs))
