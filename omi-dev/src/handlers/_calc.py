import json
from fastapi import HTTPException
from dc_core.models.db.user import DBUser
from models.responses import MinstroyRatioResponse
from settings import DEFAULT_PERIOD_1, DEFAULT_PERIOD_2, DEFAULT_REGION

caption = "Итого общая стоимость, руб,\nв том числе:"
caption_1 = "- Затраты на оборудование и материалы (МО), руб"
# 1_1 - Включая стоимость оборудования
# 1_2 - Включая стоимость материалов
caption_2 = "- Затраты на оплату труда рабочих (ЗРП), руб"
caption_3 = "- Накладные затраты, вспомогательные работы и сметная прибыль (накладные затраты МО, руб"
caption_4 = "- Затраты на эксплуатацию строительных машин и механизмов (ЭМ), руб"
caption_5 = "- Прочие расходы, руб"


def get_minstroy_ratio(self, region, period):
    rs = self.db_layer.directories.get_minstroy_by_params(region=region, period=period)
    if not rs:
        raise HTTPException(404, f"Не найден коэффициент пересчета по {region}, {period} квартал")

    return MinstroyRatioResponse(**rs)


def chapters_calc(self, chapters, period, region):
    # if period == DEFAULT_PERIOD_2 and region == DEFAULT_REGION:
    #     return chapters

    fk2 = get_minstroy_ratio(self, region=DEFAULT_REGION, period=DEFAULT_PERIOD_1).k2
    tk2 = get_minstroy_ratio(self, region, period).k2

    for key, val in chapters.items():
        # print(key, fk2, tk2)
        val = round(val / fk2 * tk2, 4)
        # print(key, val)
        chapters[key] = val

    return chapters


def create_estimate(self, id: int, response: json, is_filter_null_values: bool, current_user: DBUser):
    prices = self.db_layer.directories.get_prices(period="2024-2", user_id=current_user.id, full=False)
    questions = self.db_layer.registries.get_questions(questionnaire_object_id=id, full=False)
    sections = self.db_layer.directories.get_sections()

    rs = self.db_layer.directories.get_section_cost_ratio_by_id(id=0)
    total_ratio = float(rs.get("value"))
    # total_ratio = 1

    a128 = None     # Произвести расчет для разделов - «Сведения об инженерном оборудовании, о сетях инженерно-технического обеспечения, перечень инженерно-технических мероприятий, содержание технологических решений»
    a130 = None     # Период применения индексов изменения сметной стоимости (квартал и год)
    a131 = None     # Регион строительства

    for question in questions:
        if question.get("param") == 'a128':
            a128 = question.get("val")
        elif question.get("param") == 'a130':
            a130 = question.get("val")
        elif question.get("param") == 'a131':
            a131 = question.get("val")

    if not a128:
        a128 = "Да"
    if not a130:
        a130 = DEFAULT_PERIOD_2
    if not a131:
        a131 = DEFAULT_REGION

    print(a130, a131)

    # получаем коэффициенты для расчета стоимости материалов
    # текущий коэффициент
    rs = self.db_layer.directories.get_minstroy_by_params(region=DEFAULT_REGION, period=DEFAULT_PERIOD_2)
    if not rs:
        raise HTTPException(404, f"Не найден коэффициент пересчета по {DEFAULT_REGION}, {DEFAULT_PERIOD_2} квартал")
    # print(rs)
    cur_ratio = rs.get("k2") or 0
    # целевой коэффициент
    rs = self.db_layer.directories.get_minstroy_by_params(region=a131, period=a130)
    if not rs:
        raise HTTPException(404, f"Не найден коэффициент пересчета по {a131}, {a130} квартал")
    # print(rs)
    tar_ratio = rs.get("k2") or 0

    sections_tech = []
    section_time = {}
    chapters = {}
    chapter2_cost = None
    model_sections = response["sections"]
    for model_section in model_sections:
        model_type = model_section.get("model").get("model_type")
        if model_type == "tech":
            sections_tech.append(model_section)
        elif model_type == "price":
            predicts = model_section.get("predicts")
            for predict in predicts:
                chapter = str(predict.get("chapter"))
                if chapter:
                    chapters[chapter] = predict.get("quantity") * total_ratio
                if chapter == "2":
                    chapter2_cost = predict.get("quantity")
        elif model_type == "time":
            section_time = model_section

    chapters = chapters_calc(self, chapters=chapters, period=a130, region=a131)

    # print(chapters)
    # print("chapter2_cost", chapter2_cost)

    sections_new = []
    model_cost = round(response.get("result").get("total_cost"), 2)
    # chapter2_cost = chapters.get("2")
    # caption = "Итого общая стоимость, руб,\nв том числе"
    total_estimate_cost_1 = 0
    total_estimate_cost_2 = 0
    total_estimate_cost_3 = 0
    total_estimate_cost_4 = 0
    total_estimate_cost_5 = 0
    total_resource_cost_1 = 0
    total_resource_cost_2 = 0
    total_resource_cost_3 = 0
    total_resource_cost_4 = 0
    total_resource_cost_5 = 0
    total_average_cost_1 = 0
    total_average_cost_2 = 0
    total_average_cost_3 = 0
    total_average_cost_4 = 0
    total_average_cost_5 = 0
    num = 0
    for section in sections:
        section_code = section.get("section_code")
        section_name = section.get("section_name")
        # print(section_code)
        section_ratio = section.get("value")
        if section_ratio == None:
            continue
        section_ratio = float(section_ratio)
        section_cost_est = round(chapter2_cost * total_ratio * section_ratio, 2)
        # print(section_code, f"{chapter2_cost} * {total_ratio} * {section_ratio} =", section_cost_est)
        section_cost_res = 0
        section["section_cost_est"] = section_cost_est

        # section_name = ""
        # model_section = ""
        found = False
        for model_section in model_sections:
            if model_section.get("section_code") == section_code:
                # section_name = model_section.get("name")
                found = True
                break

        if not found:
            continue
            # print(section_code, section_name, f"{chapter2_cost} * {total_ratio} * {section_ratio} =", section_cost_est)
            # print(section_code, section_cost_est)

        if not section_name:
            print("ПРОПУСК !")
            continue

        section["section_name"] = section_name

        if "Раздел ИОС. Подраздел" in section_name and a128 == "Нет":
            print("ПРОПУСК !!")
            continue

        # check visible condition
        visible = True
        for question in questions:
            if question.get("section_code") == section_code:
                if question.get("val") == "Нет":
                    visible = False
                break
        if visible == False:
            print("ПРОПУСК !!!")
            continue

        # create element_types list
        element_types = []
        element_types_new = []

        predicts = sorted(model_section.get("predicts"), key=lambda d: d['element_type'], reverse=True)
        for predict in predicts:
            if predict.get("element_type") not in element_types:
                element_types.append(predict.get("element_type"))

        pos_1 = 0
        predicts = sorted(model_section.get("predicts"), key=lambda d: d['name'])
        for element_type in element_types:
            pos_1 += 1
            pos_2 = 0
            predicts_new = []

            for predict in predicts:
                if predict.get("element_type") == element_type:
                    if (is_filter_null_values and predict.get("quantity") > 0) or not is_filter_null_values:
                        pos_2 += 1
                        element_price = None

                        for price in prices:
                            if price.get("elementtype_name") == predict.get("element_dict"):
                                    # and price.get("element_type") == predict.get("element_type")
                                    # and price.get("unit") == predict.get("unit")):
                                element_price = round(float(price.get("value")) / 1.18 / cur_ratio * tar_ratio, 2)
                                break
                        if element_price == None:
                            # print(f'{predict.get("element_dict")}. Price not found!')
                            element_price = 0

                        element_cost = round(predict.get("quantity") * element_price, 2)
                        section_cost_res = round(section_cost_res + element_cost, 2)
                        num += 1
                        row = {
                            "num": num,
                            "pos": f"{pos_1}{'.'}{pos_2}",
                            "name": predict.get("name"),
                            "unit": predict.get("unit"),
                            "price": element_price,
                            "quantity": predict.get("quantity"),
                            "element_dict": predict.get("element_dict"),
                            "element_type": predict.get("element_type"),
                            "cost": element_cost
                        }
                        # print(section_code, predict.get("name"), element_cost)
                        predicts_new.append(row)
            element_types_new.append(
                {
                    "name": element_type,
                    "pos": str(pos_1),
                    "predicts": predicts_new
                }
            )

        # print(section_code, section_cost_res)

        section["section_cost_res"] = section_cost_res
        # print(" - ", section_code, section_cost_est, section_cost_res)
        section_costs = detailed_calc(self, section, period=a130, region=a131)
        # print(section_costs)
        estimate = section_costs.get("estimate")
        resource = section_costs.get("resource")
        average = section_costs.get("average")

        total_estimate_cost_1 = round(total_estimate_cost_1 + estimate.get("cost_1").get("value"), 2)
        total_estimate_cost_2 = round(total_estimate_cost_2 + estimate.get("cost_2").get("value"), 2)
        total_estimate_cost_3 = round(total_estimate_cost_3 + estimate.get("cost_3").get("value"), 2)
        total_estimate_cost_4 = round(total_estimate_cost_4 + estimate.get("cost_4").get("value"), 2)
        total_estimate_cost_5 = round(total_estimate_cost_5 + estimate.get("cost_5").get("value"), 2)
        total_estimate_cost = round(total_estimate_cost_1 +
                                    total_estimate_cost_2 +
                                    total_estimate_cost_3 +
                                    total_estimate_cost_4 +
                                    total_estimate_cost_5, 2)
        # print("total_estimate", total_estimate)

        total_resource_cost_1 = round(total_resource_cost_1 + resource.get("cost_1").get("value"), 2)
        total_resource_cost_2 = round(total_resource_cost_2 + resource.get("cost_2").get("value"), 2)
        total_resource_cost_3 = round(total_resource_cost_3 + resource.get("cost_3").get("value"), 2)
        total_resource_cost_4 = round(total_resource_cost_4 + resource.get("cost_4").get("value"), 2)
        total_resource_cost_5 = round(total_resource_cost_5 + resource.get("cost_5").get("value"), 2)
        total_resource_cost = round(total_resource_cost_1 +
                                    total_resource_cost_2 +
                                    total_resource_cost_3 +
                                    total_resource_cost_4 +
                                    total_resource_cost_5, 2)
        # print("total_resource", total_resource)

        total_average_cost_1 = round(total_average_cost_1 + average.get("cost_1").get("value"), 2)
        total_average_cost_2 = round(total_average_cost_2 + average.get("cost_2").get("value"), 2)
        total_average_cost_3 = round(total_average_cost_3 + average.get("cost_3").get("value"), 2)
        total_average_cost_4 = round(total_average_cost_4 + average.get("cost_4").get("value"), 2)
        total_average_cost_5 = round(total_average_cost_5 + average.get("cost_5").get("value"), 2)
        total_average_cost = round(total_average_cost_1 +
                                    total_average_cost_2 +
                                    total_average_cost_3 +
                                    total_average_cost_4 +
                                    total_average_cost_5, 2)
        # print("total_resource", total_resource)

        total_estimate = {
            "cost": {
                "name": caption,
                "value": total_estimate_cost,
            },
            "cost_1": {
                "name": caption_1,
                "value": total_estimate_cost_1,
            },
            "cost_2": {
                "name": caption_2,
                "value": total_estimate_cost_2,
            },
            "cost_3": {
                "name": caption_3,
                "value": total_estimate_cost_3,
            },
            "cost_4": {
                "name": caption_4,
                "value": total_estimate_cost_4,
            },
            "cost_5": {
                "name": caption_5,
                "value": total_estimate_cost_5,
            },
        }
        total_resource = {
            "cost": {
                "name": caption,
                "value": total_resource_cost,
            },
            "cost_1": {
                "name": caption_1,
                "value": total_resource_cost_1,
            },
            "cost_2": {
                "name": caption_2,
                "value": total_resource_cost_2,
            },
            "cost_3": {
                "name": caption_3,
                "value": total_resource_cost_3,
            },
            "cost_4": {
                "name": caption_4,
                "value": total_resource_cost_4,
            },
            "cost_5": {
                "name": caption_5,
                "value": total_resource_cost_5,
            },
        }
        total_average = {
            "cost": {
                "name": caption,
                "value": total_average_cost,
            },
            "cost_1": {
                "name": caption_1,
                "value": total_average_cost_1,
            },
            "cost_2": {
                "name": caption_2,
                "value": total_average_cost_2,
            },
            "cost_3": {
                "name": caption_3,
                "value": total_average_cost_3,
            },
            "cost_4": {
                "name": caption_4,
                "value": total_average_cost_4,
            },
            "cost_5": {
                "name": caption_5,
                "value": total_average_cost_5,
            },
        }


        # расчет сметной стоимости материалов и оборудования
        for element_type in element_types_new:
            predicts = element_type.get("predicts")
            for predict in predicts:
                cost = predict.get("cost")
                if cost:
                    cost_est = round(cost / resource.get("cost_1").get("value") * estimate.get("cost_1").get("value"), 2)
                    # print(" - ", section_code, cost, resource.get("cost_1").get("value"), estimate.get("cost_1").get("value"))
                else:
                    cost_est = 0
                predict["cost_est"] = cost_est



        sections_new.append(
            {
                "name": section_name,
                "code": section_code,
                "cost": estimate.get("cost").get("value"),
                "estimate": estimate,
                "resource": resource,
                "average": average,
                "element_types": element_types_new,
            }
        )

    # print("====", sections)
    # calculation = calc_e(self, sections=sections, period=a130, region=a131)
    # print(calculation)

    # total_costs = {
    #     "estimate": total_estimate,
    #     "resource": total_resource,
    #     "average": total_average,
    # }

    result = {
        "model_cost": model_cost,
        # "total_cost": total_cost_res,
        # "total_cost_est": total_estimate.get("cost"),
        # "total_cost_res": total_resource.get("cost"),
        # "total_cost_avg": total_average.get("cost"),
        "estimate": total_estimate,
        "resource": total_resource,
        "average": total_average,
        # "total_ratio": total_ratio
    }

    result, summary = get_basic_params(self, id, chapters, result, sections_tech, section_time, current_user)
    # result = {}
    # summary = {}

    estimate = {
        "result": result,
        "sections": sections_new,
        "summary": summary
    }

    rs = self.db_layer.registries.recording_response(
        id=id,
        response=json.dumps(response),
        estimate=json.dumps(estimate)
    )

    if not rs:
        raise HTTPException(404, f"Строка с ID={id} не найдена")

    try:
        self.db_layer.commit()
    except Exception as e:
        self.db_layer.rollback()
        raise e

    return estimate




# def calc_e(self, sections, period, region):
#     cost_est = {
#         "1": 0,
#         "2": 0,
#         "3": 0,
#         "4": 0,
#         "5": 0,
#         "6": 0,
#         '7': 0
#     }
#     cost_res = {
#         "1": 0,
#         "2": 0,
#         "3": 0,
#         "4": 0,
#         "5": 0,
#         "6": 0,
#         '7': 0
#     }
#
#     for section in sections:
#         section_code = section.get("section_code")
#         if not section_code:
#             continue
#         k1 = section.get("k1") or 0
#         k2 = section.get("k2") or 0
#         k3 = section.get("k3") or 0
#         k4 = section.get("k4") or 0
#         k5 = section.get("k5") or 0
#         section_cost_est = section.get("section_cost_est") or 0
#         section_cost_res = (section.get("section_cost_res") or 0) / 1.18
#         # print(section_code, section_cost_res)
#
#         # 1 - Затраты на оборудование и материалы (МО)
#         # 2 - Включая стоимость оборудования
#         # 3 - Включая стоимость материалов
#         # 4 - Затраты на оплату труда рабочих (ЗРП), руб
#         # 5 - Накладные затраты, вспомогательные работы и сметная прибыль (накладные затраты МО
#         # 6 - Затраты на эксплуатацию строительных машин и механизмов (ЭМ), руб
#         # 7 - Прочие расходы, руб
#
#         section_cost_est_1 = section_cost_est / (k1 + k2 + k4 + k5 + 1)
#         section_cost_est_2 = section_cost_est_1 * k3
#         section_cost_est_3 = section_cost_est_1 * (1 - k3)
#         section_cost_est_4 = section_cost_est_1 * k1
#         section_cost_est_5 = section_cost_est_1 * k2
#         section_cost_est_6 = section_cost_est_1 * k4
#         section_cost_est_7 = section_cost_est_1 * k5
#
#         section_cost_res_1 = section_cost_res
#         section_cost_res_2 = section_cost_res_1 * k3
#         section_cost_res_3 = section_cost_res_1 * (1 - k3)
#         section_cost_res_4 = section_cost_res_1 * k1
#         section_cost_res_5 = section_cost_res_1 * k2
#         section_cost_res_6 = section_cost_res_1 * k4
#         section_cost_res_7 = section_cost_res_1 * k5
#
#         if period != DEFAULT_PERIOD and region != DEFAULT_REGION:
#             rs = self.db_layer.directories.get_minstroy_by_params(region=DEFAULT_REGION, period=DEFAULT_PERIOD)
#             if not rs:
#                 raise HTTPException(404, f"Не найден коэффициент пересчета по {DEFAULT_REGION}, {DEFAULT_PERIOD} квартал")
#             fk1 = rs.get("k1") or 0
#             fk2 = rs.get("k2") or 0
#             fk3 = rs.get("k3") or 0
#             fk4 = rs.get("k4") or 0
#             fk5 = 0.75 * fk1 + 0.25 * fk2
#
#             section_cost_est_2 = section_cost_est_2 / fk4
#             section_cost_est_3 = section_cost_est_3 / fk2
#             section_cost_est_1 = section_cost_est_2 + section_cost_est_3
#             section_cost_est_4 = section_cost_est_4 / fk1
#             section_cost_est_5 = section_cost_est_5 / fk5
#             section_cost_est_6 = section_cost_est_6 / fk3
#             section_cost_est_7 = section_cost_est_7 / fk1
#
#             section_cost_res_2 = section_cost_res_2 / fk4
#             section_cost_res_3 = section_cost_res_3 / fk2
#             section_cost_res_1 = section_cost_res_2 + section_cost_res_3
#             section_cost_res_4 = section_cost_res_4 / fk1
#             section_cost_res_5 = section_cost_res_5 / fk5
#             section_cost_res_6 = section_cost_res_6 / fk3
#             section_cost_res_7 = section_cost_res_7 / fk1
#
#             rs = self.db_layer.directories.get_minstroy_by_params(region=region, period=period)
#             if not rs:
#                 raise HTTPException(404, f"Не найден коэффициент пересчета по {region}, {period} квартал")
#             tk1 = rs.get("k1") or 0
#             tk2 = rs.get("k2") or 0
#             tk3 = rs.get("k3") or 0
#             tk4 = rs.get("k4") or 0
#             tk5 = 0.75 * tk1 + 0.25 * tk2
#
#             section_cost_est_2 = section_cost_est_2 * tk4
#             section_cost_est_3 = section_cost_est_3 * tk2
#             section_cost_est_1 = section_cost_est_2 + section_cost_est_3
#             section_cost_est_4 = section_cost_est_4 * tk1
#             section_cost_est_5 = section_cost_est_5 * tk5
#             section_cost_est_6 = section_cost_est_6 * tk3
#             section_cost_est_7 = section_cost_est_7 * tk1
#
#             section_cost_res_2 = section_cost_res_2 * tk4
#             section_cost_res_3 = section_cost_res_3 * tk2
#             section_cost_res_1 = section_cost_res_2 + section_cost_res_3
#             section_cost_res_4 = section_cost_res_4 * tk1
#             section_cost_res_5 = section_cost_res_5 * tk5
#             section_cost_res_6 = section_cost_res_6 * tk3
#             section_cost_res_7 = section_cost_res_7 * tk1
#
#         cost_est["1"] = cost_est["1"] + section_cost_est_1
#         cost_est["2"] = cost_est["2"] + section_cost_est_2
#         cost_est["3"] = cost_est["3"] + section_cost_est_3
#         cost_est["4"] = cost_est["4"] + section_cost_est_4
#         cost_est["5"] = cost_est["5"] + section_cost_est_5
#         cost_est["6"] = cost_est["6"] + section_cost_est_6
#         cost_est["7"] = cost_est["7"] + section_cost_est_7
#
#         cost_res["1"] = cost_res["1"] + section_cost_res_1
#         cost_res["2"] = cost_res["2"] + section_cost_res_2
#         cost_res["3"] = cost_res["3"] + section_cost_res_3
#         cost_res["4"] = cost_res["4"] + section_cost_res_4
#         cost_res["5"] = cost_res["5"] + section_cost_res_5
#         cost_res["6"] = cost_res["6"] + section_cost_res_6
#         cost_res["7"] = cost_res["7"] + section_cost_res_7
#
#     return {
#         "cost_est": cost_est,
#         "cost_res": cost_res
#     }


def detailed_calc(self, section, period, region):
    k1 = section.get("k1") or 0
    k2 = section.get("k2") or 0
    k3 = section.get("k3") or 0
    k4 = section.get("k4") or 0
    k5 = section.get("k5") or 0
    # print("k1..k5", k1, k2, k3, k4, k5)
    section_cost_est = section.get("section_cost_est") or 0
    # print(section.get("section_code"), section.get("section_cost_res"))
    section_cost_res = section.get("section_cost_res") or 0
    # section_cost_res = (section.get("section_cost_res") or 0) / 1.18
    # print(section.get("section_code"), section_cost_res)

    estimate = {
        "cost": {
            "name": caption,
            "value": 0,
        },
        "cost_1": {
            "name": caption_1,
            "value": 0,
        },
        "cost_2": {
            "name": caption_2,
            "value": 0,
        },
        "cost_3": {
            "name": caption_3,
            "value": 0,
        },
        "cost_4": {
            "name": caption_4,
            "value": 0,
        },
        "cost_5": {
            "name": caption_5,
            "value": 0,
        },
    }
    resource = {
        "cost": {
            "name": caption,
            "value": 0,
        },
        "cost_1": {
            "name": caption_1,
            "value": 0,
        },
        "cost_2": {
            "name": caption_2,
            "value": 0,
        },
        "cost_3": {
            "name": caption_3,
            "value": 0,
        },
        "cost_4": {
            "name": caption_4,
            "value": 0,
        },
        "cost_5": {
            "name": caption_5,
            "value": 0,
        },
    }
    average = {
        "cost": {
            "name": caption,
            "value": 0,
        },
        "cost_1": {
            "name": caption_1,
            "value": 0,
        },
        "cost_2": {
            "name": caption_2,
            "value": 0,
        },
        "cost_3": {
            "name": caption_3,
            "value": 0,
        },
        "cost_4": {
            "name": caption_4,
            "value": 0,
        },
        "cost_5": {
            "name": caption_5,
            "value": 0,
        },
    }

    estimate_cost_1 = section_cost_est / (k1 + k2 + k4 + k5 + 1)
    estimate_cost_1_1 = estimate_cost_1 * k3
    estimate_cost_1_2 = estimate_cost_1 * (1 - k3)
    estimate_cost_2 = estimate_cost_1 * k1
    estimate_cost_3 = estimate_cost_1 * k2
    estimate_cost_4 = estimate_cost_1 * k4
    estimate_cost_5 = estimate_cost_1 * k5


    # print(section.get("section_code"), "STEP 5")
    # print("estimate_cost_1", estimate_cost_1)
    # print("estimate_cost_1_1", estimate_cost_1_1)
    # print("estimate_cost_1_2", estimate_cost_1_2)
    # print("estimate_cost_2", estimate_cost_2)
    # print("estimate_cost_3", estimate_cost_3)
    # print("estimate_cost_4", estimate_cost_4)
    # print("estimate_cost_5", estimate_cost_5)

    resource_cost_1 = section_cost_res
    # print(section.get("section_code"), resource_cost_1)
    resource_cost_1_1 = resource_cost_1 * k3
    resource_cost_1_2 = resource_cost_1 * (1 - k3)
    resource_cost_2 = resource_cost_1 * k1
    resource_cost_3 = resource_cost_1 * k2
    resource_cost_4 = resource_cost_1 * k4
    resource_cost_5 = resource_cost_1 * k5

    # print("estimate", estimate)
    # print("resource", resource)

    # print(period, DEFAULT_PERIOD, region, DEFAULT_REGION)

    # if period != DEFAULT_PERIOD or region != DEFAULT_REGION:

    # коэффициенты для сметного расчета
    rs = self.db_layer.directories.get_minstroy_by_params(region=DEFAULT_REGION, period=DEFAULT_PERIOD_1)
    if not rs:
        raise HTTPException(404, f"Не найден коэффициент пересчета по {DEFAULT_REGION}, {DEFAULT_PERIOD_1} квартал")
    # print(rs)
    fk1 = rs.get("k1") or 0
    fk2 = rs.get("k2") or 0
    fk3 = rs.get("k3") or 0
    fk4 = rs.get("k4") or 0
    fk5 = 0.75 * fk1 + 0.25 * fk2

    # коэффициенты для ресурсного расчета. стоимость материалов делится
    rs = self.db_layer.directories.get_minstroy_by_params(region=DEFAULT_REGION, period=DEFAULT_PERIOD_2)
    if not rs:
        raise HTTPException(404, f"Не найден коэффициент пересчета по {DEFAULT_REGION}, {DEFAULT_PERIOD_2} квартал")
    # print(rs)
    fkr1 = rs.get("k1") or 0
    fkr2 = rs.get("k2") or 0
    fkr3 = rs.get("k3") or 0
    fkr4 = rs.get("k4") or 0
    fkr5 = 0.75 * fkr1 + 0.25 * fkr2

    # print("fk1..fk5", fk1, fk2, fk3, fk4, fk5)

    estimate_cost_1_1 = estimate_cost_1_1 / fk4
    estimate_cost_1_2 = estimate_cost_1_2 / fk2
    estimate_cost_1 = estimate_cost_1_1 + estimate_cost_1_2
    estimate_cost_2 = estimate_cost_2 / fk1
    estimate_cost_3 = estimate_cost_3 / fk5
    estimate_cost_4 = estimate_cost_4 / fk3
    estimate_cost_5 = estimate_cost_5 / fk1

    # print(section.get("section_code"), "STEP 6")
    # print("estimate_cost_1", estimate_cost_1)
    # print("estimate_cost_1_1", estimate_cost_1_1)
    # print("estimate_cost_1_2", estimate_cost_1_2)
    # print("estimate_cost_2", estimate_cost_2)
    # print("estimate_cost_3", estimate_cost_3)
    # print("estimate_cost_4", estimate_cost_4)
    # print("estimate_cost_5", estimate_cost_5)

    resource_cost_1_1 = resource_cost_1_1 / fkr4
    resource_cost_1_2 = resource_cost_1_2 / fkr2
    resource_cost_1 = resource_cost_1_1 + resource_cost_1_2
    # print(section.get("section_code"), resource_cost_1)
    resource_cost_2 = resource_cost_2 / fkr1
    resource_cost_3 = resource_cost_3 / fkr5
    resource_cost_4 = resource_cost_4 / fkr3
    resource_cost_5 = resource_cost_5 / fkr1

    # print("estimate", estimate)
    # print("resource", resource)

    rs = self.db_layer.directories.get_minstroy_by_params(region=region, period=period)
    if not rs:
        raise HTTPException(404, f"Не найден коэффициент пересчета по {region}, {period} квартал")
    tk1 = rs.get("k1") or 0
    tk2 = rs.get("k2") or 0
    tk3 = rs.get("k3") or 0
    tk4 = rs.get("k4") or 0
    tk5 = 0.75 * tk1 + 0.25 * tk2

    estimate_cost_1_1 = round(estimate_cost_1_1 * tk4, 2)
    estimate_cost_1_2 = round(estimate_cost_1_2 * tk2, 2)
    estimate_cost_1 = round(estimate_cost_1_1 + estimate_cost_1_2, 2)
    estimate_cost_2 = round(estimate_cost_2 * tk1, 2)
    estimate_cost_3 = round(estimate_cost_3 * tk5, 2)
    estimate_cost_4 = round(estimate_cost_4 * tk3, 2)
    estimate_cost_5 = round(estimate_cost_5 * tk1, 2)

    # print(section.get("section_code"), "STEP 7")
    # print("estimate_cost_1", estimate_cost_1)
    # print("estimate_cost_1_1", estimate_cost_1_1)
    # print("estimate_cost_1_2", estimate_cost_1_2)
    # print("estimate_cost_2", estimate_cost_2)
    # print("estimate_cost_3", estimate_cost_3)
    # print("estimate_cost_4", estimate_cost_4)
    # print("estimate_cost_5", estimate_cost_5)

    resource_cost_1_1 = round(resource_cost_1_1 * tk4, 2)
    resource_cost_1_2 = round(resource_cost_1_2 * tk2, 2)
    resource_cost_1 = round(resource_cost_1_1 + resource_cost_1_2, 2)
    # print(section.get("section_code"), resource_cost_1)
    resource_cost_2 = round(resource_cost_2 * tk1, 2)
    resource_cost_3 = round(resource_cost_3 * tk5, 2)
    resource_cost_4 = round(resource_cost_4 * tk3, 2)
    resource_cost_5 = round(resource_cost_5 * tk1, 2)



    estimate_cost = round(estimate_cost_1 +
                          estimate_cost_2 +
                          estimate_cost_3 +
                          estimate_cost_4 +
                          estimate_cost_5, 2)

    # print(section.get("section_name"), "estimate_cost", estimate_cost)

    estimate["cost"]["value"] = estimate_cost
    estimate["cost_1"]["value"] = estimate_cost_1
    estimate["cost_2"]["value"] = estimate_cost_2
    estimate["cost_3"]["value"] = estimate_cost_3
    estimate["cost_4"]["value"] = estimate_cost_4
    estimate["cost_5"]["value"] = estimate_cost_5

    resource_cost = round(resource_cost_1 +
                          resource_cost_2 +
                          resource_cost_3 +
                          resource_cost_4 +
                          resource_cost_5, 2)
    resource["cost"]["value"] = resource_cost
    resource["cost_1"]["value"] = resource_cost_1
    resource["cost_2"]["value"] = resource_cost_2
    resource["cost_3"]["value"] = resource_cost_3
    resource["cost_4"]["value"] = resource_cost_4
    resource["cost_5"]["value"] = resource_cost_5

    average["cost"]["value"] = round((estimate_cost + resource_cost) / 2, 2)
    average["cost_1"]["value"] = round((estimate_cost_1 + resource_cost_1) / 2, 2)
    average["cost_2"]["value"] = round((estimate_cost_2 + resource_cost_2) / 2, 2)
    average["cost_3"]["value"] = round((estimate_cost_3 + resource_cost_3) / 2, 2)
    average["cost_4"]["value"] = round((estimate_cost_4 + resource_cost_4) / 2, 2)
    average["cost_5"]["value"] = round((estimate_cost_5 + resource_cost_5) / 2, 2)


    # print("estimate", estimate)
    # print("resource", resource)

    return {
        "estimate": estimate,
        "resource": resource,
        "average": average,
    }






def get_basic_params(self, questionnaire_object_id, chapters, total_costs, sections_tech, section_time, current_user):
    questions = self.db_layer.registries.get_questions(questionnaire_object_id=questionnaire_object_id, full=False)
    if 4 in current_user.role_ids:
        user_id = None
    else:
        user_id = current_user.id
    rs = self.db_layer.registries.get_questionnaire_object_by_id(id=questionnaire_object_id, calc_type=None, user_id=user_id)
    params = rs.get("params")

    # cost_3 = 0
    # cost_4 = 0
    # cost_5 = 0
    #
    # for section in sections:
    #     if section.get("code") == "AR":
    #         # 3 Раздел  - Архитектурные решения
    #         cost_3 = section.get("cost")
    #     elif section.get("code") == "KR":
    #         cost_4 = section.get("cost")
    #     elif "Раздел ИОС. Подраздел" in section.get("name"):
    #         cost_5 += section.get("cost")

    data = {}
    for b in params:
        data.update(b)
    a12 = data.get("a12") or 0
    a72 = data.get("a72") or 0
    a8 = data.get("a8") or 0
    a126 = data.get("a126") or 0
    a127 = data.get("a127") or 0

    # cost_6 = a126 * (a12 + a72)
    # cost_7 = a127 * a8
    # cost_1 = cost_3 + cost_4 + cost_5 + cost_6 + cost_7
    # cost_2 = round(cost_1 / a8, 3)

    params_1 = [
        {"param": "a1", "pos": "1"},
        {"param": "a2", "pos": "2"},
        {"param": "a3", "pos": "3"},
    ]
    params_2 = [
        {"param": "a7", "pos": "1"},
        {"param": "a8", "pos": "2"},
        {"param": "a9", "pos": "3"},
        {"param": "a10", "pos": "3.1"},
        {"param": "a11", "pos": "3.2"},
        {"param": "a12", "pos": "4"},
        {"param": "a13", "pos": "5"},
        {"param": "a5", "pos": "6"},
        {"param": "a18", "pos": "6.1"},
        {"param": "a21", "pos": "6.2"},
        {"param": "a25", "pos": "7"},
        {"param": "a26", "pos": "7.1"},
        {"param": "a27", "pos": "7.2"},
        {"param": "a36", "pos": "8.1"},
        {"param": "a37", "pos": "8.2"},
        {"param": "a38", "pos": "8.3"}
    ]

    elements = []
    for element in params_1:
        for question in questions:
            if question.get("param") == element.get("param"):
                row = {
                    "pos": element.get("pos"),
                    "name": question.get("name"),
                    "value": question.get("val")
                }
                elements.append(row)
                break

    section_1 = {
        "name": "Блок 1 Установочные данные объекта",
        "elements": elements
    }

    elements = []
    for element in params_2:
        if data.get("a25") == "Нет" or data.get("a25") == None:
            if element.get("param") == "a26":
                continue
            if element.get("param") == "a27":
                continue
        if data.get("a10") == 0 or data.get("a10") == None:
            if element.get("param") == "a36":
                continue
            if element.get("param") == "a37":
                continue
            if element.get("param") == "a38":
                continue
        for question in questions:
            if question.get("param") == element.get("param"):
                value = data.get(element.get("param"))
                if element.get("param") == "a18":
                    a18 = value
                    if a18:
                        value = ""
                        for i, building in enumerate(a18):
                            if len(value) > 0:
                                value += ', '
                            value += "Зд." + str(i + 1) + "-" + str(building)
                elif element.get("param") == "a21":
                    a21 = value
                    if a21:
                        value = ""
                        for i, building in enumerate(a21):
                            for k, section in enumerate(building):
                                if section is not None:
                                    if len(value) > 0:
                                        value += ', '
                                    value += "Зд." + str(i + 1) + "_Секц." + str(k + 1) + "-" + str(section)
                row = {
                    "pos": element.get("pos"),
                    "name": question.get("name"),
                    "unit": question.get("unit"),
                    "value": value,
                    "datatype": question.get("datatype")
                }
                elements.append(row)
                break
    section_2 = {
        "name": "Блок 2 Основные технико-экономические показатели объекта",
        "elements": elements
    }




    chapters_cost = 0
    for key, val in chapters.items():
        if key != "2":
            chapters_cost += val

    # print(sections)
    estimate = total_costs.get("estimate")
    resource = total_costs.get("resource")
    average = total_costs.get("average")

    estimate_value = round(estimate.get("cost").get("value"), 2)
    resource_value = round(resource.get("cost").get("value"), 2)
    average_value = round(average.get("cost").get("value"), 2)

    estimate_total = round(chapters_cost + estimate.get("cost").get("value"), 2)
    resource_total = round(chapters_cost + resource.get("cost").get("value"), 2)
    average_total = round(chapters_cost + average.get("cost").get("value"), 2)

    # print("estimate", estimate.get("cost").get("value"))

    total_costs["estimate"]["cost"]["value"] = estimate_total
    total_costs["resource"]["cost"]["value"] = resource_total
    total_costs["average"]["cost"]["value"] = average_total
    total_costs["total_cost"] = estimate_total

    # print("estimate", estimate.get("cost").get("value"))


    # elements = []
    section_3 = {
        "name": "Блок 3 Инвестиционные показатели",
        "elements": [
            {
                "pos": "1",
                "name": "Общая стоимость реализации объекта",
                "unit": "руб.",
                "estimate": {
                    "value": estimate_total,
                    "value_per_unit": round(estimate_total / a8, 2),
                },
                "resource": {
                    "value": resource_total,
                    "value_per_unit": round(resource_total / a8, 2),
                },
                "average": {
                    "value": average_total,
                    "value_per_unit": round(average_total / a8, 2),
                },
                "datatype": "float",
                # temporary
                "value": estimate_total
            },
            {
                "pos": "1.1",
                "name": "Глава 1 Подготовка территории строительства",
                "unit": "руб.",
                "value": round(chapters.get("1"), 2),
                "value_per_unit": round(chapters.get("1") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.2",
                "name": "Глава 2 Основные объекты строительства",
                "unit": "руб.",
                "estimate": {
                    "value": estimate_value,
                    "value_per_unit": round(estimate_value / a8, 2),
                },
                "resource": {
                    "value": resource_value,
                    "value_per_unit": round(resource_value / a8, 2),
                },
                "average": {
                    "value": average_value,
                    "value_per_unit": round(average_value / a8, 2),
                },
                "datatype": "float",
                # temporary
                "value": estimate_value
            },
            {
                "pos": "1.2.1",
                "name": "Затраты на оборудование и материалы (МО)",
                "unit": "руб.",
                "estimate": {
                    "value": estimate.get("cost_1").get("value"),
                },
                "resource": {
                    "value": resource.get("cost_1").get("value"),
                },
                "average": {
                    "value": average.get("cost_1").get("value"),
                },
                "datatype": "float",
                # temporary
                "value": estimate.get("cost_1").get("value")
            },
            {
                "pos": "1.2.2",
                "name": "Затраты на оплату труда рабочих (ЗРП)",
                "unit": "руб.",
                "estimate": {
                    "value": estimate.get("cost_2").get("value"),
                },
                "resource": {
                    "value": resource.get("cost_2").get("value"),
                },
                "average": {
                    "value": average.get("cost_2").get("value"),
                },
                "datatype": "float",
                # temporary
                "value": estimate.get("cost_2").get("value")
            },
            {
                "pos": "1.2.3",
                "name": "Накладные затраты, вспомогательные работы и сметная прибыль",
                "unit": "руб.",
                "estimate": {
                    "value": estimate.get("cost_3").get("value"),
                },
                "resource": {
                    "value": resource.get("cost_3").get("value"),
                },
                "average": {
                    "value": average.get("cost_3").get("value"),
                },
                "datatype": "float",
                # temporary
                "value": estimate.get("cost_3").get("value")
            },
            {
                "pos": "1.2.4",
                "name": "Затраты на эксплуатацию строительных машин и механизмов (ЭМ)",
                "unit": "руб.",
                "estimate": {
                    "value": estimate.get("cost_4").get("value"),
                },
                "resource": {
                    "value": resource.get("cost_4").get("value"),
                },
                "average": {
                    "value": average.get("cost_4").get("value"),
                },
                "datatype": "float",
                # temporary
                "value": estimate.get("cost_4").get("value")
            },
            {
                "pos": "1.2.5",
                "name": "Прочие расходы",
                "unit": "руб.",
                "estimate": {
                    "value": estimate.get("cost_5").get("value"),
                },
                "resource": {
                    "value": resource.get("cost_5").get("value"),
                },
                "average": {
                    "value": average.get("cost_5").get("value"),
                },
                "datatype": "float",
                # temporary
                "value": estimate.get("cost_5").get("value")
            },
            {
                "pos": "1.3",
                "name": "Глава 3 Объекты подсобного и обслуживающего назначения",
                "unit": "руб.",
                "value": round(chapters.get("3"), 2),
                "value_per_unit": round(chapters.get("3") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.4",
                "name": "Глава 4 Объекты энергетического хозяйства",
                "unit": "руб.",
                "value": round(chapters.get("4"), 2),
                "value_per_unit": round(chapters.get("4") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.5",
                "name": "Глава 5 Объекты транспортного хозяйства и связи",
                "unit": "руб.",
                "value": round(chapters.get("5"), 2),
                "value_per_unit": round(chapters.get("5") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.6",
                "name": "Глава 6 Наружные сети и сооружения водоснабжения, водоотведения, теплоснабжения и газоснабжения",
                "unit": "руб.",
                "value": round(chapters.get("6"), 2),
                "value_per_unit": round(chapters.get("6") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.7",
                "name": "Глава 7 Благоустройство и озеленение территории",
                "unit": "руб.",
                "value": round(chapters.get("7"), 2),
                "value_per_unit": round(chapters.get("7") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.8",
                "name": "Глава 8 Временные здания и сооружения",
                "unit": "руб.",
                "value": round(chapters.get("8"), 2),
                "value_per_unit": round(chapters.get("8") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.9",
                "name": "Глава 9 Прочие работы и затраты",
                "unit": "руб.",
                "value": round(chapters.get("9"), 2),
                "value_per_unit": round(chapters.get("9") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.10",
                "name": "Глава 10 Содержание службы Заказчика.Строительный контроль",
                "unit": "руб.",
                "value": round(chapters.get("10"), 2),
                "value_per_unit": round(chapters.get("10") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.11",
                "name": "Глава 11 Подготовка эксплуатационных кадров для строящегося объекта капитального строительства",
                "unit": "руб.",
                "value": round(chapters.get("11"), 2),
                "value_per_unit": round(chapters.get("11") / a8, 2),
                "datatype": "float"
            },
            {
                "pos": "1.12",
                "name": "Глава 12. Публичный технологический и ценовой аудит, подготовка обоснования инвестиций, осуществляемых в инвестиционный проект по созданию объекта капитального строительства, в отношении которого планируется заключение контракта, предметом которого является одновременно выполнение работ по проектированию, строительству и вводу в эксплуатацию объекта капитального строительства, технологический и ценовой аудит такого обоснования инвестиций, аудит проектной документации, проектные и изыскательские работы",
                "unit": "руб.",
                "value": round(chapters.get("12"), 2),
                "value_per_unit": round(chapters.get("12") / a8, 2),
                "datatype": "float"
            },
        ]
    }

    # print(section_time)

    if section_time:
        section_3["elements"].append(
            {
                "pos": "2",
                "name": "Продолжительность строительства:",
                "unit": "",
                "value": None,
                "value_per_unit": None,
                "datatype": "str"
            }
        )
        for n, predict in enumerate(section_time["predicts"]):
            section_3["elements"].append(
                {
                    "pos": f"2.{n+1}",
                    "name": predict.get("element_dict"),
                    "unit": predict.get("unit"),
                    "value": predict.get("quantity"),
                    "value_per_unit": None,
                    "datatype": "float"
                }
            )

    elements = []
    pos_1 = 0
    for section in sections_tech:
        pos_1 += 1
        pos_2 = 0
        predicts = section.get("predicts")
        params = []
        for predict in predicts:
            pos_2 += 1
            value = predict.get("quantity")
            if value == None:
                value = 0
            row = {
                "pos": f"{pos_1}.{pos_2}" if predict.get("name") != "Общая тепловая мощность" else None,
                "name": predict.get("name"),
                "unit": predict.get("unit"),
                "value": float(value),
                "datatype": "float"
            }
            params.append(row)

        elements.append(
            {
                "pos": f"{pos_1}",
                "name": section.get("name"),
                "params": params
            }
        )
    section_4 = {
        "name": "Блок 4 Технические условия на технологическое присоединение",
        "elements": elements
    }

    result = [
        section_1,
        section_2,
        section_3,
        section_4
    ]

    return total_costs, result
