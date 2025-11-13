# import requests
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from typing import List, Optional
from fastapi import APIRouter, Depends
from utils.depends import get_db, get_settings, get_current_user
from handlers.services import ServicesHandler
from handlers.storage import StorageHandler
from models.requests.export import ReportFormat
from models.requests import CalcType
from dc_core.models.requests import (
    CreateStatementRequest,
    UpdateStatementRequest,
)

from dc_core.models.responses import (
    StatementResponse,
    AttachmentResponse,
)

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/request")
async def get_request(
        id: int,
        current_user=Depends(get_current_user),
        db=Depends(get_db)):
    return ServicesHandler(db).get_request(id, current_user)

@router.get("/response")
async def get_response(
        id: int,
        is_filter_null_values: Optional[bool] = None,
        current_user=Depends(get_current_user),
        db=Depends(get_db)):
    return ServicesHandler(db).get_response(id, is_filter_null_values, current_user)

@router.get("/export")
async def export_to_file(
        id: int,
        fmt: ReportFormat,
        calc_type: CalcType = CalcType.estimate,
        current_user=Depends(get_current_user),
        db=Depends(get_db)):
    return ServicesHandler(db).export(id, fmt, calc_type.value, current_user)

@router.post("/uploadfile")
async def create_upload_file(
        statement_guid: str,
        files: List[UploadFile],
        current_user=Depends(get_current_user),
        db=Depends(get_db),
        settings=Depends(get_settings)):
    return StorageHandler(db, settings=settings).uploadfile(statement_guid, files, current_user)

@router.get("/downloadfile")
async def download_file(
        guid: str,
        current_user=Depends(get_current_user),
        db=Depends(get_db),
        settings=Depends(get_settings)):
    return StorageHandler(db, settings=settings).downloadfile(guid)

@router.delete("/deletefile")
async def delete_file(
        filename: Optional[str] = None,
        current_user=Depends(get_current_user),
        db=Depends(get_db),
        settings=Depends(get_settings)):
    return StorageHandler(db, settings=settings).deletefile(filename)

@router.get("/uploaded_list")
async def uploaded_list(
        path: Optional[str] = None,
        current_user=Depends(get_current_user),
        db=Depends(get_db),
        settings=Depends(get_settings)):
    return StorageHandler(db, settings=settings).uploaded_list(path)

@router.get("/statement", response_model=List[StatementResponse])
async def get_statements(
        id: Optional[int] = None,
        state_id: Optional[int] = None,
        current_user=Depends(get_current_user),
        db=Depends(get_db)):
    return StorageHandler(db).get_statements(id, state_id, current_user)

@router.post("/statement", response_model=StatementResponse)
async def create_statement(
        data: CreateStatementRequest,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
        settings=Depends(get_settings)
):
    return StorageHandler(db, settings=settings).create_statement(data, current_user)

@router.put("/statement", response_model=StatementResponse)
async def update_statement(
        data: UpdateStatementRequest,
        bt: BackgroundTasks,
        current_user=Depends(get_current_user),
        db=Depends(get_db),
        settings=Depends(get_settings)
):
    return StorageHandler(db, settings=settings, background_tasks=bt).update_statement(data, current_user)

@router.delete("/statement", response_model=StatementResponse)
async def delete_statement(
        id: int,
        current_user=Depends(get_current_user),
        db=Depends(get_db)):
    return StorageHandler(db).delete_statement(id, current_user)

@router.get("/attachment")
async def get_attachments_by_statement_guid(
        statement_guid: str,
        current_user=Depends(get_current_user),
        db=Depends(get_db)):
    return StorageHandler(db).get_attachments_by_statement_guid(statement_guid, current_user)

@router.delete("/attachment", response_model=AttachmentResponse)
async def delete_attachment(
        guid: str,
        current_user=Depends(get_current_user),
        db=Depends(get_db),
        settings=Depends(get_settings)):
    return StorageHandler(db, settings=settings).delete_attachment(guid, current_user)


@router.post("/file/import")
async def import_file(
        file: UploadFile,
        object_numbers: str = None,
        questionnaire_id: int = 1,
        update: bool = False,
        current_user=Depends(get_current_user),
        db=Depends(get_db),
        settings=Depends(get_settings),
):
    return ServicesHandler(db, settings=settings).import_file(
        file=file,
        object_numbers=object_numbers,
        questionnaire_id=questionnaire_id,
        update=update,
        current_user=current_user,
    )
