# -*- coding: utf-8 -*-
import typing as t
from datetime import date
from pydantic import BaseModel, EmailStr

__all__ = (
    "CreateSectionCostRatioRequest",
    "UpdateSectionCostRatioRequest",
)


class CreateSectionCostRatioRequest(BaseModel):
    section_code: str
    value: float


class UpdateSectionCostRatioRequest(BaseModel):
    id: int
    value: float
