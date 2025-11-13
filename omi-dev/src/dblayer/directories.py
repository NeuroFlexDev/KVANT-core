# -*- coding: utf-8 -*-
from dc_core.dblayer import DBLayer

__all__ = ("DirectoriesDBLayer",)


class DirectoriesDBLayer(DBLayer):
    def get_states(self, **kwargs):
        return self.map_all(self.queries.get_states(self.db, kwargs))

    def get_roles(self, **kwargs):
        return self.map_all(self.queries.get_roles(self.db, kwargs))

    def get_activities(self, **kwargs):
        return self.map_all(self.queries.get_activities(self.db, kwargs))

    def get_section_cost_ratio_by_id(self, **kwargs):
        return self.map_one(self.queries.get_section_cost_ratio_by_id(self.db, kwargs))

    def get_section_cost_ratio(self, **kwargs):
        return self.map_all(self.queries.get_section_cost_ratio(self.db, kwargs))

    def get_sections(self, **kwargs):
        return self.map_all(self.queries.get_sections(self.db, kwargs))

    def get_section_cost_ratio_sum(self, **kwargs):
        return self.map_one(self.queries.get_section_cost_ratio_sum(self.db, kwargs))

    def update_section_cost_ratio(self, **kwargs):
        return self.map_one(self.queries.update_section_cost_ratio(self.db, kwargs))

    def section_cost_ratio_sync(self, **kwargs):
        return self.map_one(self.queries.section_cost_ratio_sync(self.db, kwargs))

    def get_minstroy_by_params(self, **kwargs):
        return self.map_one(self.queries.get_minstroy_by_params(self.db, kwargs))

    def get_prices(self, **kwargs):
        return self.map_all(self.queries.get_prices(self.db, kwargs))
