# -*- coding: utf-8 -*-
import json
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from fastapi import HTTPException

from dc_core.models.db.user import DBUser

from handlers import BaseHandler
from models.requests.questionnaire import (
    CreateFormRequest,
    SectionPayload,
    UpdateFormRequest,
    UpsertSectionRequest,
)
from models.responses.questionnaire import (
    QuestionnaireFormDetailResponse,
    QuestionnaireFormSummaryResponse,
    QuestionnaireSectionResponse,
    SectionProgressResponse,
)

__all__ = ("QuestionnaireHandler",)


class QuestionnaireHandler(BaseHandler):
    DEFAULT_SECTIONS: List[SectionPayload] = [
        SectionPayload(section_key="general", title="Общие сведения", order_index=0, data={}),
        SectionPayload(section_key="architecture", title="Архитектурные параметры", order_index=1, data={}),
        SectionPayload(section_key="summary", title="Сводные показатели", order_index=2, data={}),
        SectionPayload(section_key="engineering", title="Инженерные решения", order_index=3, data={}),
        SectionPayload(section_key="composition", title="Состав разделов", order_index=4, data={}),
    ]

    SECTION_DEFAULTS: Dict[str, SectionPayload] = {
        section.section_key: section for section in DEFAULT_SECTIONS
    }

    @staticmethod
    def _ensure_dict(value: Any) -> Dict[str, Any]:
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        if isinstance(value, str) and value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return {}
        return {}

    @staticmethod
    def _json_param(value: Optional[Dict[str, Any]]) -> Optional[str]:
        if value is None:
            return None
        return json.dumps(value)

    @classmethod
    def _resolve_section_defaults(cls, payload: SectionPayload, fallback_index: int) -> SectionPayload:
        defaults = cls.SECTION_DEFAULTS.get(payload.section_key)
        title = payload.title or (defaults.title if defaults else None)
        order_index = fallback_index if payload.order_index is None else payload.order_index
        if defaults and payload.order_index is None:
            order_index = defaults.order_index if defaults.order_index is not None else fallback_index
        return SectionPayload(
            section_key=payload.section_key,
            title=title,
            order_index=order_index,
            data=payload.data or {},
            is_completed=payload.is_completed,
            completed_at=payload.completed_at,
        )

    def list_forms(self, current_user: DBUser) -> List[QuestionnaireFormSummaryResponse]:
        forms = self.db_layer.questionnaire.list_forms(user_id=current_user.id)
        result: List[QuestionnaireFormSummaryResponse] = []
        for form in forms:
            sections = self.db_layer.questionnaire.list_sections(form_id=form["id"])
            progress = self._build_progress(sections)
            payload = self._prepare_form_payload(form)
            payload["progress"] = progress.dict()
            result.append(QuestionnaireFormSummaryResponse(**payload))
        return result

    def create_form(self, data: CreateFormRequest, current_user: DBUser) -> QuestionnaireFormDetailResponse:
        sections_payload = data.sections or self.DEFAULT_SECTIONS

        try:
            form_record = self.db_layer.questionnaire.create_form(
                user_id=current_user.id,
                title=data.title,
                description=data.description,
                status=data.status,
                current_step=data.current_step,
                metadata=self._json_param(data.metadata),
            )

            for idx, section in enumerate(sections_payload):
                resolved = self._resolve_section_defaults(section, idx)
                self._upsert_section_record(
                    form_id=form_record["id"],
                    section_key=resolved.section_key,
                    title=resolved.title,
                    order_index=resolved.order_index if resolved.order_index is not None else idx,
                    data=resolved.data,
                    is_completed=resolved.is_completed if resolved.is_completed is not None else False,
                    completed_at=resolved.completed_at,
                )

            self.db_layer.commit()
        except Exception:
            self.db_layer.rollback()
            raise

        return self.get_form(form_record["id"], current_user)

    def get_form(self, form_id: int, current_user: DBUser) -> QuestionnaireFormDetailResponse:
        form_record = self.db_layer.questionnaire.get_form_by_id(
            form_id=form_id,
            user_id=current_user.id,
        )
        if not form_record:
            raise HTTPException(status_code=404, detail="Форма не найдена")

        sections_records = self.db_layer.questionnaire.list_sections(form_id=form_id)
        form_payload = self._prepare_form_payload(form_record)
        form_payload["sections"] = [self._prepare_section_payload(section) for section in sections_records]

        return QuestionnaireFormDetailResponse(**form_payload)

    def update_form(
        self,
        form_id: int,
        data: UpdateFormRequest,
        current_user: DBUser,
    ) -> QuestionnaireFormDetailResponse:
        existing = self.db_layer.questionnaire.get_form_by_id(
            form_id=form_id,
            user_id=current_user.id,
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Форма не найдена")

        try:
            updated = self.db_layer.questionnaire.update_form(
                form_id=form_id,
                user_id=current_user.id,
                title=data.title,
                description=data.description,
                status=data.status,
                current_step=data.current_step,
                metadata=self._json_param(data.metadata),
            )
            if not updated:
                raise HTTPException(status_code=404, detail="Форма не найдена")
            self.db_layer.commit()
        except Exception:
            self.db_layer.rollback()
            raise

        return self.get_form(form_id, current_user)

    def delete_form(self, form_id: int, current_user: DBUser) -> QuestionnaireFormSummaryResponse:
        existing = self.db_layer.questionnaire.get_form_by_id(
            form_id=form_id,
            user_id=current_user.id,
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Форма не найдена")

        try:
            deleted = self.db_layer.questionnaire.mark_form_deleted(
                form_id=form_id,
                user_id=current_user.id,
            )
            if not deleted:
                raise HTTPException(status_code=404, detail="Форма не найдена")
            self.db_layer.commit()
        except Exception:
            self.db_layer.rollback()
            raise

        sections = self.db_layer.questionnaire.list_sections(form_id=form_id)
        payload = self._prepare_form_payload(existing)
        payload["progress"] = self._build_progress(sections).dict()
        return QuestionnaireFormSummaryResponse(**payload)

    def upsert_section(
        self,
        form_id: int,
        section_key: str,
        request: UpsertSectionRequest,
        current_user: DBUser,
    ) -> QuestionnaireSectionResponse:
        form_record = self.db_layer.questionnaire.get_form_by_id(
            form_id=form_id,
            user_id=current_user.id,
        )
        if not form_record:
            raise HTTPException(status_code=404, detail="Форма не найдена")

        existing_section = self.db_layer.questionnaire.get_section(
            form_id=form_id,
            section_key=section_key,
        )

        defaults = self.SECTION_DEFAULTS.get(section_key)

        base_data: Dict[str, Any] = {}
        if existing_section:
            base_data = self._ensure_dict(existing_section.get("data"))
        elif defaults:
            base_data = defaults.data or {}

        merged_data = {**base_data, **(request.data or {})}

        if request.is_completed is None:
            is_completed = existing_section.get("is_completed") if existing_section else False
        else:
            is_completed = request.is_completed

        completed_at = request.completed_at
        now_utc = datetime.utcnow()

        if existing_section:
            current_completed_at = existing_section.get("completed_at")
            if request.is_completed is None:
                completed_at = current_completed_at
            elif request.is_completed:
                completed_at = completed_at or current_completed_at or now_utc
            else:
                completed_at = None
        else:
            if is_completed:
                completed_at = completed_at or now_utc

        resolved_title = request.title or (existing_section.get("title") if existing_section else (defaults.title if defaults else None))
        resolved_order = request.order_index
        if resolved_order is None:
            if existing_section and existing_section.get("order_index") is not None:
                resolved_order = existing_section["order_index"]
            elif defaults and defaults.order_index is not None:
                resolved_order = defaults.order_index
            else:
                resolved_order = 0

        try:
            record = self._upsert_section_record(
                form_id=form_id,
                section_key=section_key,
                title=resolved_title,
                order_index=resolved_order,
                data=merged_data,
                is_completed=is_completed,
                completed_at=completed_at,
            )

            self.db_layer.commit()
        except Exception:
            self.db_layer.rollback()
            raise

        return QuestionnaireSectionResponse(**self._prepare_section_payload(record))

    def _upsert_section_record(
        self,
        *,
        form_id: int,
        section_key: str,
        title: Optional[str],
        order_index: Optional[int],
        data: Dict[str, Any],
        is_completed: bool,
        completed_at: Optional[datetime],
    ) -> Dict[str, Any]:
        return self.db_layer.questionnaire.upsert_section(
            form_id=form_id,
            section_key=section_key,
            title=title,
            order_index=order_index,
            data=self._json_param(data),
            is_completed=is_completed,
            completed_at=completed_at,
        )

    def _prepare_form_payload(self, record: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(record)
        payload.pop("user_id", None)
        payload.pop("is_deleted", None)
        payload["metadata"] = self._ensure_dict(payload.get("metadata"))
        return payload

    def _prepare_section_payload(self, record: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(record)
        payload["data"] = self._ensure_dict(payload.get("data"))
        return payload

    @staticmethod
    def _build_progress(sections: Iterable[Dict[str, Any]]) -> SectionProgressResponse:
        total = 0
        completed = 0
        for section in sections:
            total += 1
            if section.get("is_completed"):
                completed += 1
        return SectionProgressResponse(total=total, completed=completed)
