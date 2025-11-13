# -*- coding: utf-8 -*-
import typing as t
from datetime import date
from fastapi import APIRouter, Depends
from utils.depends import get_current_user, get_db
from handlers.logs import LogsHandler
from models.responses import LogResponse

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/logs", response_model=t.List[LogResponse])
async def get_logs(
        user_id: t.Optional[int] = None,
        # table_name: t.Optional[str] = 'dir.questionnaire_object',
        record_id: t.Optional[int] = None,
        date_from: t.Optional[date] = None,
        date_to: t.Optional[date] = None,
        action: t.Optional[str] = None,
        # current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    table_name = None
    return LogsHandler(db).get_logs(user_id, table_name, record_id, date_from, date_to, action)