# -*- coding: utf-8 -*-
from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

__all__ = (
    "ObjectResponse",
    "QuestionnaireResponse",
    "QuestionResponse",
    "ElementResponse",
)


class ObjectResponse(BaseModel):
    id: int
    state_id: int
    name: str
    creator_id: Optional[int]
    createdate: datetime
    modifier_id: Optional[int]
    modifydate: Optional[datetime]
    guid: str
    address: str


class QuestionnaireResponse(BaseModel):
    pass


class QuestionResponse(BaseModel):
    id: int
    pos: str
    name: str
    parent_id: Optional[int]
    value: Optional[list]
    datatype: Optional[str]
    param: Optional[str]
    validation: Optional[list]
    condition: Optional[list]


class ElementResponse(BaseModel):
    uid: UUID
    # id: int
    # state_id: int
    # creator_id: Optional[int]
    # createdate: datetime
    # modifier_id: Optional[int]
    # modifydate: Optional[datetime]
    # guid: str
    # class_type: str
    element_name: str
    element_type: str
    unit: str
    price: float
