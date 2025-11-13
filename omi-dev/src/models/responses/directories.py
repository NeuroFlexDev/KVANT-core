# -*- coding: utf-8 -*-
import typing as t
from datetime import date, datetime
from pydantic import BaseModel, EmailStr

__all__ = (
    "StatesResponse",
    "RolesResponse",
    "ActivitiesResponse",
    "SectionCostRatioResponse",
    "PriceResponse",
    "PricesResponse",
    "MinstroyRatioResponse",
)


class StatesResponse(BaseModel):
    id: int
    name: str

class RolesResponse(BaseModel):
    id: int
    state_id: int
    name: str
    creator_id: t.Optional[int]
    createdate: datetime
    modifier_id: t.Optional[int]
    modifydate: t.Optional[datetime]
    guid: str

class ActivitiesResponse(BaseModel):
    id: int
    state_id: int
    name: str
    creator_id: t.Optional[int]
    createdate: datetime
    modifier_id: t.Optional[int]
    modifydate: t.Optional[datetime]
    guid: str

class SectionCostRatioResponse(BaseModel):
    id: int
    state_id: int
    section_code: str
    section_name: t.Optional[str]
    creator_id: t.Optional[int]
    createdate: datetime
    modifier_id: t.Optional[int]
    modifydate: t.Optional[datetime]
    guid: str
    value: t.Optional[float]
    k1: t.Optional[float]
    k2: t.Optional[float]
    k3: t.Optional[float]
    k4: t.Optional[float]
    k5: t.Optional[float]

class PriceResponse(BaseModel):
    id: t.Optional[int]
    state_id: t.Optional[int]
    creator_id: t.Optional[int]
    createdate: t.Optional[datetime]
    modifier_id: t.Optional[int]
    modifydate: t.Optional[datetime]
    guid: t.Optional[str]
    elementtype_name: str
    element_name: t.Optional[str]
    unit: t.Optional[str]
    value_ws: t.Optional[float]
    quantity_ws: t.Optional[float]
    value: float
    ratio: float
    url: t.Optional[str]
    period: t.Optional[str]
    base_value: t.Optional[float]

class PricesResponse(BaseModel):
    element_type: str
    unit: t.Optional[str]
    value: float

class MinstroyRatioResponse(BaseModel):
    region: str
    period: str
    k1: float
    k2: float
    k3: float
    k4: float
