# -*- coding: utf-8 -*-
import typing as t

from fastapi import APIRouter, Depends
from utils.depends import get_current_user, get_db
from handlers.directories import DirectoriesHandler
from models.requests import UpdateSectionCostRatioRequest
from models.responses import (
    StatesResponse,
    RolesResponse,
    ActivitiesResponse,
    PriceResponse,
    PricesResponse,
)
from models.responses import SectionCostRatioResponse

router = APIRouter(prefix="/directories", tags=["directories"])


@router.get("/states", response_model=t.List[StatesResponse])
async def get_states(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).get_states()


@router.get("/roles", response_model=t.List[RolesResponse])
async def get_roles(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).get_roles()


@router.get("/activities", response_model=t.List[ActivitiesResponse])
async def get_activities(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).get_activities()


@router.get("/section_cost_ratio/{id}", response_model=SectionCostRatioResponse)
async def get_section_cost_ratio_by_id(
    id: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).get_section_cost_ratio_by_id(id)

@router.get("/section_cost_ratio", response_model=t.List[SectionCostRatioResponse])
async def get_section_cost_ratio(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).get_section_cost_ratio()

@router.get("/section_cost_ratio_sum")
async def get_section_cost_ratio_sum(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).get_section_cost_ratio_sum()

@router.put("/section_cost_ratio", response_model=SectionCostRatioResponse)
async def update_section_cost_ratio(
    data: UpdateSectionCostRatioRequest,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).update_section_cost_ratio(data, current_user)

# @router.put("/section_cost_ratio/sync", response_model=t.List[SectionCostRatioResponse])
# async def section_cost_ratio_sync(
#     current_user=Depends(get_current_user),
#     db=Depends(get_db),
# ):
#     return DirectoriesHandler(db).section_cost_ratio_sync(current_user)


@router.get("/prices", response_model=t.List[PriceResponse])
async def get_prices(
    period: str = "2024-2",
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return DirectoriesHandler(db).get_prices(period, current_user)
