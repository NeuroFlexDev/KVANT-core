import json
from typing import List, Optional

from fastapi import HTTPException

from dc_core.models.db.user import DBUser
from models.requests import (
    CalcType,
    CreateObjectRequest,
    CreateQuestionnaireObjectRequest,
    UpdateObjectRequest,
    UpdateQuestionnaireObjectRequest,
    CreateElementRequest,
    UpdateElementRequest,
)
from models.responses import (
    ObjectResponse,
    ElementResponse
)

from handlers import BaseHandler

__all__ = ("RegistriesHandler",)


class RegistriesHandler(BaseHandler):
    def get_objects(self, id: int, current_user: DBUser) -> List[ObjectResponse]:
        if 4 in current_user.role_ids:
            user_id = None
        else:
            user_id = current_user.id
        if id:
            rs = self.db_layer.registries.get_object_by_id(id=id, user_id=user_id)
        else:
            rs = self.db_layer.registries.get_objects(user_id=user_id)
        return [ObjectResponse(**r) for r in rs] if rs else []

    def create_object(self, data: CreateObjectRequest, current_user: DBUser) -> ObjectResponse:
        rs = self.db_layer.registries.create_object(
            name=data.name, address=data.address, user_id=current_user.id
        )

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return ObjectResponse(**rs)

    def update_object(self, data: UpdateObjectRequest, current_user: DBUser) -> ObjectResponse:
        rs = self.db_layer.registries.update_object(
            id=data.id, name=data.name, address=data.address, user_id=current_user.id
        )

        if not rs:
            raise HTTPException(404, f"Объект с ID={data.id} не найден")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return ObjectResponse(**rs)

    def delete_object(self, id: int, current_user: DBUser) -> ObjectResponse:
        rs = self.db_layer.registries.delete_object(id=id, user_id=current_user.id)

        if not rs:
            raise HTTPException(404, f"Объект с ID={id} не найден")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return rs

    def conv(self, aa: list): # преобразование условий формата filterBuilder в строку
        if not aa:
            return None
        signs = ["=", "<>", ">", "<", ">=", "<="]
        string = ""
        if aa[1] in signs:
            aa = [aa]
        for i in aa:
            if type(i) is list:
                if i[1] in signs:
                    if type(i[2]) is int:
                        casting = "::float"
                    else:
                        casting = ""
                    string += "(a.params::json ->> '" + i[0] + "')" + casting + i[1]
                    if type(i[2]) is str:
                        string += "'" + i[2] + "'"
                    else:
                        string += str(i[2])
                else:
                    string += self.conv(i)
            else:
                string += " " + i + " "
        return string

    def check_on_fill(self, value):
        if type(value) is list and value != []:
            for i in value:
                if self.check_on_fill(i) == False:
                    return False
        elif value in (None, "", []):
            return False

        return True

    def isfloat(self, str):
        if type(str) == list:
            for s in str:
                if self.isfloat(s):
                    return True
        if isinstance(str, float):
            return True
        else:
            return False

    def get_questionnaire_object_status(self, body: List, questionnaire_object_id: int):
        state = []

        # формирование справочника параметров с условиями
        questions = self.db_layer.registries.get_questions(questionnaire_object_id=questionnaire_object_id, full=False)
        conditions = dict()
        datatypes = dict()
        for question in questions:
            param = question.get("param")
            condition = question.get("condition")
            condition = self.conv(condition)
            if condition:
                conditions[param] = condition

            datatypes[param] = question.get("datatype")

        # преобразование массива json параметров в один
        data = {}
        for b in body:
            data.update(b)
        data.pop("desc")


        # Подсчет количества пустых параметров с учетом условий
        # for data in body:
        for key, val in data.items():
            if val == None:
                condition = conditions.get(key)
                if condition:
                    pp = {
                        "params": json.dumps(data),
                        "condition": condition
                    }
                    rs = self.db_layer.registries.check_condition(pp)
                    if rs[0] == True:
                        state.append("Параметр " + key + " не заполнен")
                else:
                    state.append("Параметр " + key + " не заполнен")
            else:
                if not self.check_on_fill(val):
                    state.append("Параметр " + key + " не заполнен")
                if datatypes.get(key) == 'int':
                    if self.isfloat(val):
                        raise HTTPException(415, f"Ошибка типа данных {val}. Параметр {key} должен быть целым.")

        if state == []:
            state_id = 1 # "Заполнен"
        else:
            state_id = 0 # "На заполнении"

        return state_id, state

    def get_questionnaire_objects(self, id: int, object_id: int, calc_type: CalcType, current_user: DBUser):
        if 4 in current_user.role_ids:
            user_id = None
        else:
            user_id = current_user.id
        if id != None:
            rs = self.db_layer.registries.get_questionnaire_object_by_id(id=id, calc_type=calc_type, user_id=user_id)
        elif object_id != None:
            rs = self.db_layer.registries.get_questionnaire_object_by_object_id(object_id=object_id, calc_type=calc_type, user_id=user_id)
        else:
            rs = self.db_layer.registries.get_questionnaire_objects(calc_type=calc_type, user_id=user_id)
        return rs if rs else []

    def create_questionnaire_object(
        self, data: CreateQuestionnaireObjectRequest, current_user: DBUser
    ):
        rs = self.db_layer.registries.create_questionnaire_object(
            name=data.name,
            questionnaire_id=data.questionnaire_id,
            object_id=data.object_id,
            user_id=current_user.id,
        )

        self.db_layer.logs.create_log(
            table_name="dir.questionnaire_object",
            record_id=rs.get("id"),
            action="create",
            user_id=current_user.id
        )

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return rs

    def copy_questionnaire_object(
            self, questionnaire_object_id: int, current_user: DBUser
    ):
        rs = self.db_layer.registries.get_questionnaire_object_by_id(
            id=questionnaire_object_id,
            calc_type=None,
            user_id=current_user.id
        )
        if not rs:
            raise HTTPException(404, f"Опросный лист с ID={questionnaire_object_id} не найден")

        rs = self.db_layer.registries.copy_questionnaire_object(
            questionnaire_object_id=questionnaire_object_id,
            user_id=current_user.id,
        )

        self.db_layer.logs.create_log(
            table_name="dir.questionnaire_object",
            record_id=rs.get("id"),
            action="copy",
            user_id=current_user.id
        )

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return rs

    def update_questionnaire_object(
        self, data: UpdateQuestionnaireObjectRequest, current_user: DBUser
    ):
        if 4 in current_user.role_ids:
            user_id = None
        else:
            user_id = current_user.id

        state_id, state = self.get_questionnaire_object_status(data.params, data.id)

        object = self.db_layer.registries.get_object_by_id(id=data.object_id, user_id=user_id)
        object_name = object[0].get("name")
        object_address = object[0].get("address")

        params = data.params
        part = [{"a2": object_address, "desc": "1.2."}]
        if "'a2'" not in str(params):
            part.extend(params)
            params = part
        part = [{"a1": object_name, "desc": "1.1."}]
        if "'a1'" not in str(params):
            part.extend(params)
            params = part

        # проверка на изменение ОЛ
        # сохраненная версия (в базе)
        rs = self.db_layer.registries.get_questionnaire_object_by_id(
            id=data.id,
            calc_type=None,
            user_id=user_id
        )
        body = rs.get("params")
        old_params = {}
        for b in body:
            old_params.update(b)
        old_params.pop("desc")
        # print("old_params", old_params)

        # новая версия
        body = params
        new_params = {}
        for b in body:
            new_params.update(b)
        new_params.pop("desc")
        # print("new_params", new_params)

        if old_params == new_params:
            print("equal")
            response = rs.get("response")
            estimate = rs.get("estimate")
        else:
            print("not equal")
            response = None
            estimate = None


        # params = json.dumps(params)


        rs = self.db_layer.registries.update_questionnaire_object(
            id=data.id,
            state_id=state_id,
            name=data.name,
            questionnaire_id=data.questionnaire_id,
            object_id=data.object_id,
            params=json.dumps(params),
            response=json.dumps(response) if response else None,
            estimate=json.dumps(estimate) if estimate else None,
            user_id=current_user.id,
        )

        if not rs:
            raise HTTPException(404, f"Строка с ID={data.id} не найдена")

        self.db_layer.logs.create_log(
            table_name="dir.questionnaire_object",
            record_id=rs.get("id"),
            action="update",
            user_id=current_user.id
        )

        try:
            self.db_layer.commit()
            rs["state"] = state
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return rs

    def delete_questionnaire_object(
        self, id: int, current_user: DBUser
    ):
        rs = self.db_layer.registries.delete_questionnaire_object(id=id, user_id=current_user.id)

        if not rs:
            raise HTTPException(404, f"Строка с ID={id} не найдена")

        self.db_layer.logs.create_log(
            table_name="dir.questionnaire_object",
            record_id=rs.get("id"),
            action="delete",
            user_id=current_user.id
        )

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return rs

    def get_questions(self, questionnaire_object_id: int):
        rs = self.db_layer.registries.get_questions(questionnaire_object_id=questionnaire_object_id, full=True)
        return [rs]


    # Elements
    def get_elements(self) -> List[ElementResponse]:
        rs = self.db_layer.registries.get_elements()
        return [ElementResponse(**r) for r in rs] if rs else []

    def create_element(self, data: CreateElementRequest, current_user: DBUser) -> ElementResponse:
        rs = self.db_layer.registries.create_element(user_id=current_user.id, **data.dict())

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return ElementResponse(**rs)

    def update_element(self, data: UpdateElementRequest, current_user: DBUser) -> List[ElementResponse]:
        rs = self.db_layer.registries.update_element(user_id=current_user.id, **data.dict())

        if rs == []:
            raise HTTPException(404, f"Элементы с UUID={data.uid} не найдены")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return [ElementResponse(**r) for r in rs] if rs else []

    def delete_element(self, id: int, current_user: DBUser) -> ElementResponse:
        rs = self.db_layer.registries.delete_element(id=id, user_id=current_user.id)

        if not rs:
            raise HTTPException(404, f"Элемент с ID={id} не найден")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return rs