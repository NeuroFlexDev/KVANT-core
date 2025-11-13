# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

__all__ = (
    "SectionProgressResponse",
    "QuestionnaireSectionResponse",
    "QuestionnaireFormSummaryResponse",
    "QuestionnaireFormDetailResponse",
)


class SectionProgressResponse(BaseModel):
    total: int = 0
    completed: int = 0


class QuestionnaireSectionResponse(BaseModel):
    id: int
    form_id: int
    section_key: str
    title: Optional[str] = None
    order_index: int
    data: Dict[str, Any] = Field(default_factory=dict)
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class _QuestionnaireFormBase(BaseModel):
    id: int
    guid: str
    title: str
    description: Optional[str] = None
    status: str
    current_step: int
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class QuestionnaireFormSummaryResponse(_QuestionnaireFormBase):
    progress: SectionProgressResponse = Field(default_factory=SectionProgressResponse)


class QuestionnaireFormDetailResponse(_QuestionnaireFormBase):
    sections: List[QuestionnaireSectionResponse] = Field(default_factory=list)
