# -*- coding: utf-8 -*-
from typing import List, Optional
from fastapi import APIRouter, Depends
from utils.depends import get_db, get_current_user
from handlers.registry import RegistriesHandler
from handlers.services import ServicesHandler

from models.requests import (
    CalcType,
    CreateObjectRequest,
    CreateQuestionnaireObjectRequest,
    UpdateObjectRequest,
    UpdateQuestionnaireObjectRequest,
    UpdateEstimate,
    CreateElementRequest,
    UpdateElementRequest,
)
from models.responses import (
    ObjectResponse,
    ElementResponse,
)

router = APIRouter(prefix="/registries", tags=["registries"])


@router.get("/object", response_model=List[ObjectResponse])
async def get_objects(
        id: Optional[int] = None,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).get_objects(id, current_user)


@router.post("/object", response_model=ObjectResponse)
async def create_questionnaire_object(
        data: CreateObjectRequest,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).create_object(data, current_user)


@router.put("/object", response_model=ObjectResponse)
async def update_object(
        data: UpdateObjectRequest,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).update_object(data, current_user)


@router.delete("/object", response_model=ObjectResponse)
async def delete_object(
        id: int,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).delete_object(id, current_user)


@router.get("/questionnaire_object")
async def get_questionnaire_objects(
        id: Optional[int] = None,
        object_id: Optional[int] = None,
        calc_type: CalcType = CalcType.estimate,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).get_questionnaire_objects(id, object_id, calc_type.value, current_user)


@router.post("/questionnaire_object")
async def create_questionnaire_object(
        data: CreateQuestionnaireObjectRequest,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).create_questionnaire_object(data, current_user)


@router.post("/questionnaire_object/copy")
async def copy_questionnaire_object(
        questionnaire_object_id: int,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).copy_questionnaire_object(questionnaire_object_id, current_user)


@router.put("/questionnaire_object")
async def update_questionnaire_object(
        data: UpdateQuestionnaireObjectRequest,
        current_user=Depends(get_current_user),
        db=Depends(get_db),
):
    return RegistriesHandler(db).update_questionnaire_object(data, current_user)


@router.delete("/questionnaire_object")
async def delete_questionnaire_object(
        id: int,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).delete_questionnaire_object(id, current_user)


@router.get("/question")
async def get_questions(
        questionnaire_object_id: int,
        current_user=Depends(get_current_user),
        db=Depends(get_db)
):
    return RegistriesHandler(db).get_questions(questionnaire_object_id)


# @router.put("/update_estimate")
# async def update_estimate(
#     data: UpdateEstimate,
#     current_user=Depends(get_current_user),
#     db=Depends(get_db)
# ):
#     return ServicesHandler(db).update_estimate(data, current_user)


# @router.get("/element", response_model=List[ElementResponse])
# async def get_elements(
#         # id: Optional[int] = None,
#         current_user=Depends(get_current_user),
#         db=Depends(get_db)
# ):
#     return RegistriesHandler(db).get_elements()


# @router.post("/element", response_model=ElementResponse)
# async def create_element(
#         data: CreateElementRequest,
#         current_user=Depends(get_current_user),
#         db=Depends(get_db)
# ):
#     return RegistriesHandler(db).create_element(data, current_user)


# @router.put("/element", response_model=List[ElementResponse])
# async def update_element(
#         data: UpdateElementRequest,
#         current_user=Depends(get_current_user),
#         db=Depends(get_db)
# ):
#     return RegistriesHandler(db).update_element(data, current_user)


# @router.delete("/element", response_model=ElementResponse)
# async def delete_element(
#         id: int,
#         current_user=Depends(get_current_user),
#         db=Depends(get_db)
# ):
#     return RegistriesHandler(db).delete_element(id, current_user)