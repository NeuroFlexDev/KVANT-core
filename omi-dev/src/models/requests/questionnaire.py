# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

__all__ = (
    "CreateFormRequest",
    "UpdateFormRequest",
    "SectionPayload",
    "UpsertSectionRequest",
)


class SectionPayload(BaseModel):
    section_key: str
    title: Optional[str] = None
    order_index: Optional[int] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class CreateFormRequest(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    current_step: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sections: Optional[List[SectionPayload]] = None


class UpdateFormRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    current_step: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class UpsertSectionRequest(BaseModel):
    title: Optional[str] = None
    order_index: Optional[int] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
