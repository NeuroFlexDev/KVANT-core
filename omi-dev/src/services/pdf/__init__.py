import os
from io import BytesIO
from fpdf import FPDF
from fpdf.fonts import FontFace
from settings import FPDF_FONT_DIR
from fastapi.exceptions import HTTPException
from datetime import datetime

class PDF(FPDF):
    def __init__(self, caption, dt, *args, **kwargs):
        self.caption = caption
        self.dt = dt
        super().__init__(*args, **kwargs)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Calibri', '', 8)

        self.cell(0, -5, self.caption, ln=0)
        self.cell(0, -5, self.dt, align="R", ln=1)
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-5)

        self.set_font('Calibri', '', 8)

        page = 'Страница ' + str(self.page_no()) + ' из {nb}'
        self.cell(0, -5, page, 0, 0, 'C')

# class ExportPDF:
def print_text(pdf, text, font_style, font_size, **kwargs):
    pdf.set_font("Calibri", font_style, font_size)
    pdf.multi_cell(w=pdf.epw, h=pdf.font_size, txt=text, ln=1, **kwargs)

def render_toc(pdf, outline):
    pdf.x = 0
    pdf.y = 15
    pdf.set_font("Calibri", "B", size=16)
    pdf.cell(0, 0, "Содержание:", align="C", ln=1)
    pdf.y += 5
    pdf.set_font("Calibri", "", size=12)

    for section in outline:
        link = pdf.add_link()
        pdf.set_link(link, page=section.page_number)
        pdf.x = 10
        y1 = pdf.y
        pdf.multi_cell(w=pdf.epw - 10, h=1.5*pdf.font_size, txt=section.name, ln=1, link=link)
        y2 = pdf.y
        pdf.y = y1
        pdf.x = pdf.epw
        pdf.cell(txt=str(section.page_number), h=1.5*pdf.font_size, border=0, link=link)
        pdf.y = y2

def omi(id, data, params, calc_type):
    output = BytesIO()

    dt = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    caption = "Объект: " + params.get("a1") + " по адресу: " + params.get("a2")
    pdf = PDF(caption=caption, dt=dt)

    try:
        # включаем TTF шрифты, поддерживающие кириллицу
        pdf.add_font("Calibri", style="", fname=os.path.join(FPDF_FONT_DIR, "calibri.ttf"), uni=True)
        pdf.add_font("Calibri", style="B", fname=os.path.join(FPDF_FONT_DIR, "calibrib.ttf"), uni=True)
        pdf.add_font("Arial", style="", fname=os.path.join(FPDF_FONT_DIR, "arial.ttf"), uni=True)
        pdf.add_font("Arial", style="B", fname=os.path.join(FPDF_FONT_DIR, "arialbd.ttf"), uni=True)

        pdf.alias_nb_pages()

        headings_style = FontFace(emphasis="BOLD", fill_color=(200, 200, 200))

        # Титульная страница
        pdf.add_page()

        darkcyan = (38, 123, 133)
        cyan = (201, 235, 239)
        black = (0, 0, 0)
        white = (255, 255, 255)
        headings_style = FontFace(color=white, fill_color=darkcyan)
        # цвет линий таблицы
        pdf.set_draw_color(38, 123, 133)
        pdf.set_y(0)
        # pdf.set_x(-10)
        pdf.l_margin = -10

        with pdf.table(col_widths=(55, 45), text_align="LEFT",
                       line_height=pdf.font_size * 1.2, headings_style=headings_style) as table_title:

            # цвет линий таблицы
            # pdf.set_draw_color(38, 123, 133)
            # ширина линии
            # table_title.set_line_width(0.3)

            row = table_title.row()
            pdf.set_font("Arial", "B", 40)
            row.cell("KVANT", padding=(20, 20, 20, 5))
            pdf.set_font("Arial", "", 12)
            row.cell('ООО "Скрипт" ИНН 9705167220, г. Москва\n+7-926-573-32-75 info@script.engeneering\nhttps://script.engeneering | https://kvant.id')

        pdf.l_margin = 10
        # цвет текста
        pdf.set_draw_color(0, 0, 0)

        pdf.set_y(pdf.eph / 2 - 25)
        print_text(pdf, params.get("a1"), "B", 30, align="C")
        pdf.y += 5
        print_text(pdf, "Наименование объекта", "", 8, align="C")

        pdf.y += 5
        print_text(pdf, params.get("a2"), "", 18, align="C")
        pdf.y += 5
        print_text(pdf, "Адрес объекта", "", 8, align="C")

        pdf.y += 5
        print_text(pdf, params.get("a3"), "", 18, align="C")
        pdf.y += 5
        print_text(pdf, "Функциональное назначение объекта", "", 8, align="C")

        pdf.set_text_color(38, 123, 133)

        pdf.y += 20
        print_text(pdf, "Расчет сметной стоимости реализации инвестиционного объекта с помощью программного комплекса «Квант»", "", 18, align="C")

        pdf.set_text_color(0)

        pdf.set_y(pdf.eph)
        print_text(pdf, f"{datetime.now().year} г.", "", 14, align="C")

        # Автоматическое оглавление
        pdf.add_page()
        pdf.insert_toc_placeholder(render_toc)

        TABLE_HEADER = (
            ("№", "Наименование и техническая характеристика", "Значение параметра", "Ед. изм."),
        )
        TABLE_HEADER_ = (
            ("№", "Наименование и техническая характеристика", "руб", "руб/м2"),
        )

        # Краткие характеристики и показатели по ОЛ
        summaries = data.get("summary")
        for summary in summaries:
            pdf.set_font("Calibri", "B", 10)
            with pdf.table(text_align="LEFT", borders_layout="NONE", line_height=1.4 * pdf.font_size) as table_1:
                row = table_1.row()
                row.cell(summary.get("name"))
                pdf.start_section(summary.get("name"))
            if "Блок 3" not in summary.get("name"):
                with pdf.table(col_widths=(5, 60, 20, 15), text_align="CENTER",
                               cell_fill_color=cyan, cell_fill_mode="ROWS",
                               line_height=1.4 * pdf.font_size, headings_style=headings_style) as table_2:
                    for data_row in TABLE_HEADER:
                        row = table_2.row()
                        for datum in data_row:
                            row.cell(datum)
                    for element in summary.get("elements"):
                        datatype = element.get("datatype")
                        if datatype == "int":
                            value = str(element.get("value")) or ""
                        elif datatype == "float":
                            value = f'{element.get("value") or 0:,.2f}'.replace(',', ' ')
                        else:
                            value = element.get("value") or ""
                        pdf.set_font("Calibri", "", 10)
                        row = table_2.row()
                        row.cell(element.get("pos"))
                        row.cell(element.get("name"), align='L')
                        row.cell(value)
                        row.cell(element.get("unit") or "")
                        if element.get("params") is not None:
                            for param in element.get("params"):
                                row = table_2.row()
                                pos = param.get("pos")
                                row.cell(str(pos) if pos else '', align='C')
                                row.cell(param.get("name"), align='L')
                                row.cell(str(param.get("value")), align='R')
                                row.cell(param.get("unit"))
            else:
                with pdf.table(col_widths=(5, 60, 20, 15), text_align="CENTER",
                               line_height=1.4 * pdf.font_size, headings_style=headings_style,
                               cell_fill_color=cyan, cell_fill_mode="ROWS",
                               num_heading_rows=1) as table_2:
                    for data_row in TABLE_HEADER_:
                        row = table_2.row()
                        for datum in data_row:
                            row.cell(datum)
                    for element in summary.get("elements"):
                        value = element.get("value")
                        if value is None:
                            if calc_type in element:
                                value = element.get(calc_type).get("value")
                        if value is not None:
                            value = f'{value:,.2f}'.replace(',', ' ')
                        value_per_unit = element.get("value_per_unit")
                        if value_per_unit is None:
                            if calc_type in element:
                                value_per_unit = element.get(calc_type).get("value_per_unit")
                        if value_per_unit is not None:
                            value_per_unit = f'{value_per_unit:,.2f}'.replace(',', ' ')
                        pdf.set_font("Calibri", "", 10)
                        row = table_2.row()
                        row.cell(element.get("pos"), align='C')
                        row.cell(element.get("name"), align='L')
                        row.cell(value, align='R')
                        row.cell(value_per_unit, align='R')

        # Разделы ОЛ
        TABLE_HEADER = (
            ("№", "Наименование оборудования и материалов", "Кол-во", "Ед. изм.", "Сумма"),
        )

        sections = data.get("sections")
        for section in sections:
            pdf.add_page()
            pdf.set_font("Calibri", "B", 10)

            with pdf.table(text_align="LEFT", borders_layout="NONE", line_height=1.4 * pdf.font_size) as table_1:
                row = table_1.row()
                row.cell(section.get("name"))
                pdf.start_section(section.get("name"))

            with pdf.table(col_widths=(10, 50, 15, 10, 15), text_align="CENTER",
                           cell_fill_color=cyan, cell_fill_mode="ROWS",
                           line_height=1.4 * pdf.font_size, headings_style=headings_style) as table_2:
                for data_row in TABLE_HEADER:
                    row = table_2.row()
                    for datum in data_row:
                        row.cell(datum)
                for element_type in section.get("element_types"):
                    pdf.set_font("Calibri", "B", 10)
                    row = table_2.row()
                    row.cell(element_type.get("pos"))
                    row.cell(element_type.get("name"), align='L')
                    row.cell()
                    row.cell()
                    row.cell()
                    pdf.set_font("Calibri", "", 10)
                    for predict in element_type.get("predicts"):
                        row = table_2.row()
                        row.cell(predict.get("pos"))
                        row.cell(predict.get("name"), align='L')
                        row.cell(f'{predict.get("quantity"):,.0f}'.replace(',', ' '), align='R')
                        row.cell(predict.get("unit"))
                        row.cell()
                    row = table_2.row()
                    row.cell()
                    row.cell()
                    row.cell()
                    row.cell()
                    row.cell()

                pdf.set_font("Calibri", "B", 10)
                # row = table_2.row()
                # row.cell()
                # row.cell("Итого по " + section.get("name"), align='L')
                # row.cell()
                # row.cell()
                # section_cost = section.get(calc_type).get("cost").get("value")
                # row.cell(f'{section_cost:,.2f}'.replace(',', ' '), align='R')
                # pdf.set_font("Calibri", "", 10)
                # print(section.get(calc_type))
                for key in section.get(calc_type).keys():
                    cost = section.get(calc_type).get(key)
                    # print(cost)
                    row = table_2.row()
                    row.cell()
                    row.cell(cost.get("name"), align='L')
                    row.cell()
                    row.cell()
                    row.cell(f'{cost.get("value"):,.2f}'.replace(',', ' '), align='R')

        # with pdf.table(col_widths=(10, 50, 15, 10, 15), text_align="CENTER", line_height=1.4 * pdf.font_size) as table_3:
        #     pdf.set_font("Calibri", "B", 10)
        #     row = table_3.row()
        #     row.cell()
        #     row.cell()
        #     row.cell()
        #     row.cell()
        #     row.cell()

            # row.cell()
            # row.cell("ОБЩИЙ ИТОГ", align='L')
            # row.cell()
            # row.cell()
            # total_cost = data.get("result").get(calc_type).get("cost").get("value")
            # row.cell(f'{total_cost:,.2f}'.replace(',', ' '), align='R')

            # print(data.get("result").get(calc_type))
            # for key in data.get("result").get(calc_type).keys():
            #     cost = data.get("result").get(calc_type).get(key)
            #     print(cost)
            #     row = table_3.row()
            #     row.cell()
            #     row.cell(cost.get("name"), align='L')
            #     row.cell()
            #     row.cell()
            #     row.cell(f'{cost.get("value"):,.2f}'.replace(',', ' '), align='R')

        pdf.output(output)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )

    return output.getvalue()
