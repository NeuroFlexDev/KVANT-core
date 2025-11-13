import typing as t

from fastapi import HTTPException

from dc_core.models.db.user import DBUser
from models.requests import (
    UpdateSectionCostRatioRequest,
)
from models.responses import (
    StatesResponse,
    RolesResponse,
    ActivitiesResponse,
    SectionCostRatioResponse,
    PriceResponse,
    PricesResponse,
)

from handlers import BaseHandler

__all__ = ("DirectoriesHandler",)


class DirectoriesHandler(BaseHandler):
    def get_states(self) -> t.List[StatesResponse]:
        rs = self.db_layer.directories.get_states()
        if not rs:
            raise HTTPException(404, f"Объекты не найдены")
        return [StatesResponse(**r) for r in rs] if rs else []

    def get_roles(self) -> t.List[RolesResponse]:
        rs = self.db_layer.directories.get_roles()
        if not rs:
            raise HTTPException(404, f"Объекты не найдены")
        return [RolesResponse(**r) for r in rs] if rs else []

    def get_activities(self) -> t.List[ActivitiesResponse]:
        rs = self.db_layer.directories.get_activities()
        if not rs:
            raise HTTPException(404, f"Объекты не найдены")
        return [ActivitiesResponse(**r) for r in rs] if rs else []

    def get_section_cost_ratio_by_id(self, id: int) -> SectionCostRatioResponse:
        rs = self.db_layer.directories.get_section_cost_ratio_by_id(id=id)
        if not rs:
            raise HTTPException(404, f"Объект с ID={id} не найден")
        return SectionCostRatioResponse(**rs)

    def get_section_cost_ratio(self) -> t.List[SectionCostRatioResponse]:
        rs = self.db_layer.directories.get_section_cost_ratio()
        return [SectionCostRatioResponse(**r) for r in rs] if rs else []

    def get_section_cost_ratio_sum(self):
        rs = self.db_layer.directories.get_section_cost_ratio_sum()
        return rs

    def update_section_cost_ratio(self, data: UpdateSectionCostRatioRequest, current_user: DBUser) -> SectionCostRatioResponse:
        sectioncostratio = self.get_section_cost_ratio_by_id(id=data.id)

        rs = self.db_layer.directories.update_section_cost_ratio(
            id=data.id,
            value=data.value,
            user_id=current_user.id
        )

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        # return SectionCostRatioResponse(**rs)
        return self.get_section_cost_ratio_by_id(id=data.id)

    def section_cost_ratio_sync(self, current_user: DBUser) -> t.List[SectionCostRatioResponse]:
        rs = self.db_layer.directories.section_cost_ratio_sync(user_id=current_user.id)

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return self.get_section_cost_ratio()

    def get_prices(self, period: str, current_user: DBUser) -> t.List[PriceResponse]:
        rs = self.db_layer.directories.get_prices(period=period, user_id=current_user.id, full=True)
        return [PriceResponse(**r) for r in rs] if rs else []
