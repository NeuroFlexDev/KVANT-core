from pydantic import BaseModel
from typing import Optional
from enum import Enum, unique

__all__ = (
    "CreateStatementRequest",
    "UpdateStatementRequest",
    "CreateAttachmentRequest",
)


class CreateStatementRequest(BaseModel):
    statementtype_id: int

class UpdateStatementRequest(BaseModel):
    id: int
    statementtype_id: int
    topic: Optional[str]
    body: str

class CreateAttachmentRequest(BaseModel):
    path_to_object: str
    statement_id: int
    file_name: str
    # file_extension: str
    content_type: str