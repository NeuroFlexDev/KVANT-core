from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

__all__ = (
    "StatementResponse",
    "AttachmentResponse",
)


class StatementResponse(BaseModel):
    id: int
    state_id: int
    creator_id: int
    createdate: datetime
    modifier_id: Optional[int]
    modifydate: Optional[datetime]
    guid: str
    statementtype_id: int
    topic: Optional[str]
    body: Optional[str]

class AttachmentResponse(BaseModel):
    id: int
    state_id: int
    creator_id: int
    createdate: datetime
    modifier_id: Optional[int]
    modifydate: Optional[datetime]
    guid: str
    path_to_object: str
    statement_id: int
    file_name: str
    # file_extension: Optional[str]
    content_type: str
