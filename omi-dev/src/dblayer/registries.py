# -*- coding: utf-8 -*-
from dc_core.dblayer import DBLayer
from sqlalchemy.sql import text

__all__ = ("RegistriesDBLayer",)


class RegistriesDBLayer(DBLayer):
    def get_objects(self, **kwargs):
        return self.map_all(self.queries.get_objects(self.db, kwargs))

    def get_object_by_id(self, **kwargs):
        return self.map_all(self.queries.get_object_by_id(self.db, kwargs))

    def get_object_by_params(self, **kwargs):
        return self.map_one(self.queries.get_object_by_params(self.db, kwargs))

    def create_object(self, **kwargs):
        return self.map_one(self.queries.create_object(self.db, kwargs))

    def update_object(self, **kwargs):
        return self.map_one(self.queries.update_object(self.db, kwargs))

    def delete_object(self, **kwargs):
        return self.map_one(self.queries.delete_object(self.db, kwargs))

    def get_questionnaire_objects(self, **kwargs):
        return self.map_all(self.queries.get_questionnaire_objects(self.db, kwargs))

    def get_questionnaire_object_by_id(self, **kwargs):
        return self.map_one(self.queries.get_questionnaire_object_by_id(self.db, kwargs))

    def get_questionnaire_object_by_object_id(self, **kwargs):
        return self.map_all(self.queries.get_questionnaire_object_by_object_id(self.db, kwargs))

    def get_questionnaire_object_by_params(self, **kwargs):
        return self.map_one(self.queries.get_questionnaire_object_by_params(self.db, kwargs))

    def create_questionnaire_object(self, **kwargs):
        return self.map_one(self.queries.create_questionnaire_object(self.db, kwargs))

    def copy_questionnaire_object(self, **kwargs):
        return self.map_one(self.queries.copy_questionnaire_object(self.db, kwargs))

    def update_questionnaire_object(self, **kwargs):
        return self.map_one(self.queries.update_questionnaire_object(self.db, kwargs))

    def delete_questionnaire_object(self, **kwargs):
        return self.map_one(self.queries.delete_questionnaire_object(self.db, kwargs))

    def get_questions(self, **kwargs):
        return self.map_all(self.queries.get_questions(self.db, kwargs))

    def get_questions_by_questionnaire_id(self, **kwargs):
        return self.map_all(self.queries.get_questions_by_questionnaire_id(self.db, kwargs))

    def check_condition(self, params):
        query = """with a as (
            select :params as params
        )
            select $1
            from a"""

        query = query.replace("$1", params.get("condition"))
        query = text(query)

        return self.db.execute(query, params).fetchone()

    def recording_response(self, **kwargs):
        return self.map_one(self.queries.recording_response(self.db, kwargs))


    def get_elements(self, **kwargs):
        return self.map_all(self.queries.get_elements(self.db, kwargs))

    def get_element_by_id(self, **kwargs):
        return self.map_all(self.queries.get_element_by_id(self.db, kwargs))

    def create_element(self, **kwargs):
        return self.map_one(self.queries.create_element(self.db, kwargs))

    def update_element(self, **kwargs):
        return self.map_all(self.queries.update_element(self.db, kwargs))

    def delete_element(self, **kwargs):
        return self.map_one(self.queries.delete_element(self.db, kwargs))
