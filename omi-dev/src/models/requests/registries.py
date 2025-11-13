# -*- coding: utf-8 -*-
from typing import List, Optional, Dict
from enum import Enum, unique
from pydantic import BaseModel

__all__ = (
    "CreateObjectRequest",
    "UpdateObjectRequest",
    "CreateQuestionnaireObjectRequest",
    "UpdateQuestionnaireObjectRequest",
    "QuestionnaireRequest",
    "QuestionRequest",
    "UpdateEstimate",
    "CreateElementRequest",
    "UpdateElementRequest",
    "CalcType",
)


class CreateObjectRequest(BaseModel):
    name: str
    address: str


class UpdateObjectRequest(BaseModel):
    id: int
    name: str
    address: str


class CreateQuestionnaireObjectRequest(BaseModel):
    name: str
    questionnaire_id: int = 1
    object_id: int


class UpdateQuestionnaireObjectRequest(BaseModel):
    id: int
    name: str
    questionnaire_id: int = 1
    object_id: int
    params: List[Dict]


class QuestionnaireRequest(BaseModel):
    pass


class QuestionRequest(BaseModel):
    questionnaire_object_id: int


class SetPrices(BaseModel):
    num: int
    value: float


class UpdateEstimate(BaseModel):
    id: int
    prices: List[SetPrices]


class CreateElementRequest(BaseModel):
    class_type: str
    element_name: str
    element_type: str
    unit: str
    price: float


class UpdateElementRequest(BaseModel):
    # id: int
    uid: str
    # class_type: Optional[str]
    # element_name: Optional[str]
    # element_type: Optional[str]
    # unit: Optional[str]
    price: Optional[float]


@unique
class CalcType(str, Enum):
    estimate = "estimate"             # Сметный расчёт
    resource = "resource"             # Ресурсный расчёт
    average = "average"               # Расчёт средних значений
