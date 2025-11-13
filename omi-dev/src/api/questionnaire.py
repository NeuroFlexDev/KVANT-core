# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends, status

from handlers.questionnaire import QuestionnaireHandler
from models.requests.questionnaire import (
    CreateFormRequest,
    UpdateFormRequest,
    UpsertSectionRequest,
)
from models.responses.questionnaire import (
    QuestionnaireFormDetailResponse,
    QuestionnaireFormSummaryResponse,
    QuestionnaireSectionResponse,
)
from utils.depends import get_current_user, get_db

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


@router.get("/forms", response_model=List[QuestionnaireFormSummaryResponse])
async def list_forms(current_user=Depends(get_current_user), db=Depends(get_db)):
    return QuestionnaireHandler(db).list_forms(current_user)


@router.post(
    "/forms",
    response_model=QuestionnaireFormDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_form(
    data: CreateFormRequest,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return QuestionnaireHandler(db).create_form(data, current_user)


@router.get("/forms/{form_id}", response_model=QuestionnaireFormDetailResponse)
async def get_form(
    form_id: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return QuestionnaireHandler(db).get_form(form_id, current_user)


@router.patch("/forms/{form_id}", response_model=QuestionnaireFormDetailResponse)
async def update_form(
    form_id: int,
    data: UpdateFormRequest,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return QuestionnaireHandler(db).update_form(form_id, data, current_user)


@router.delete("/forms/{form_id}", response_model=QuestionnaireFormSummaryResponse)
async def delete_form(
    form_id: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return QuestionnaireHandler(db).delete_form(form_id, current_user)


@router.put(
    "/forms/{form_id}/sections/{section_key}",
    response_model=QuestionnaireSectionResponse,
)
async def upsert_section(
    form_id: int,
    section_key: str,
    request: UpsertSectionRequest,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    return QuestionnaireHandler(db).upsert_section(form_id, section_key, request, current_user)
