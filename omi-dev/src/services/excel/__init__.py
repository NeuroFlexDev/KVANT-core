import xlsxwriter
from io import BytesIO


class ExportExcel:
    def set_format(self, workbook):
        self.table_header_format = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                # "font_color": "#000000",
                "fg_color": "#e6e6e6",
                "border": 1,
                # "border_color": "#000000"
            }
        )
        self.table_header_format.set_text_wrap()

        self.header_format = workbook.add_format(
            {
                "bold": True,
                "valign": "vcenter",
                "border": 0
            }
        )
        self.header_format.set_text_wrap()

        self.cell_center_format = workbook.add_format(
            {
                "bold": 0,
                "align": "center",
                "valign": "vcenter",
                "border": 1
            }
        )
        self.cell_center_format.set_text_wrap()

        self.cell_left_format = workbook.add_format(
            {
                "bold": 0,
                "align": "left",
                "valign": "vcenter",
                "border": 1
            }
        )
        self.cell_left_format.set_text_wrap()

        self.cell_right_format = workbook.add_format(
            {
                "bold": 0,
                "align": "right",
                "valign": "vcenter",
                "border": 1,
                'num_format': '# ### ### ##0'
            }
        )
        self.cell_right_format.set_text_wrap()

        self.cell_center_bold_format = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "border": 1
            }
        )
        self.cell_center_bold_format.set_text_wrap()

        self.cell_left_bold_format = workbook.add_format(
            {
                "bold": True,
                "align": "left",
                "valign": "vcenter",
                "border": 1
            }
        )
        self.cell_left_bold_format.set_text_wrap()

        self.merge_format = workbook.add_format(
            {
                'bold': 0,
                'border': 1,
                'align': 'right',
                'valign': 'vcenter',
                'fg_color': 'white',
                'num_format': '# ### ### ##0',
                'text_wrap': True
            }
        )
        self.merge_format.set_text_wrap()

        self.merge_format_rub = workbook.add_format({
            'bold': 0,
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'fg_color': 'white',
            'num_format': '# ### ### ##0.00 ₽'})
        self.merge_format_rub.set_text_wrap()

        self.merge_format_column = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#122c6f',
            'font_color': '#ffffff',
            'border_color': '#ffffff'})
        self.merge_format_column.set_text_wrap()

        # self.money_format = workbook.add_format({'num_format': '# ##0 [$₽-419],-# ##0 [$₽-419]'})
        self.number_format = workbook.add_format(
            {
                'bold': 0,
                'border': 1,
                'align': 'right',
                'valign': 'vcenter',
                'fg_color': 'white',
                'num_format': '# ### ### ##0.00',
                'text_wrap': True
            }
        )

        self.money_format = workbook.add_format({'num_format': '# ##0 ₽;-# ##0 ₽'})
        self.percent_format = workbook.add_format({'num_format': '0 [$%]'})
        self.date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        self.default_format = workbook.add_format({'num_format': '@'})

    def omi(self, id, data, calc_type):
        output = BytesIO()

        workbook = xlsxwriter.Workbook(output)
        self.set_format(workbook)

        worksheet = workbook.add_worksheet("Сводные данные")
        sections = data.get("summary")
        row = -1
        for section in sections:
            row += 1
            worksheet.set_row(row, 30)
            worksheet.merge_range(row, 0, row, 5, section.get("name"), self.header_format)
            row += 1
            if "Блок 3" not in section.get("name"):
                worksheet.write(row, 0, "№", self.table_header_format)
                worksheet.set_column("A:A", 10)
                worksheet.write(row, 1, "Наименование и техническая характеристика", self.table_header_format)
                worksheet.set_column("B:B", 60)
                worksheet.write(row, 2, "Значение параметра", self.table_header_format)
                worksheet.set_column("C:C", 20)
                worksheet.write(row, 3, "Единица измерения", self.table_header_format)
                worksheet.set_column("D:D", 20)
                for element in section.get("elements"):
                    if element.get("datatype") == "int":
                        datatype = self.merge_format
                    elif element.get("datatype") == "float":
                        datatype = self.number_format
                    else:
                        datatype = self.cell_center_format
                    row += 1
                    worksheet.write(row, 0, element.get("pos"), self.cell_left_format)
                    worksheet.write(row, 1, element.get("name"), self.cell_left_format)
                    worksheet.write(row, 2, element.get("value"), datatype)
                    worksheet.write(row, 3, element.get("unit"), self.cell_center_format)
                    if element.get("params") is not None:
                        for param in element.get("params"):
                            if param.get("datatype") == "int":
                                datatype = self.merge_format
                            elif param.get("datatype") == "float":
                                datatype = self.number_format
                            else:
                                datatype = self.cell_right_format
                            row += 1
                            worksheet.write(row, 0, param.get("pos"), self.cell_left_format)
                            worksheet.write(row, 1, param.get("name"), self.cell_left_format)
                            worksheet.write(row, 2, param.get("value"), datatype)
                            worksheet.write(row, 3, param.get("unit"), self.cell_center_format)
            else:
                # worksheet.write(row, 0, "№", self.table_header_format)
                worksheet.merge_range(row, 0, row+1, 0, "№", self.table_header_format)
                worksheet.set_column("A:A", 10)
                # worksheet.write(row, 1, "Наименование и техническая характеристика", self.table_header_format)
                worksheet.merge_range(row, 1, row + 1, 1, "Наименование и техническая характеристика", self.table_header_format)
                worksheet.set_column("B:B", 60)
                # worksheet.write(row, 2, "Сметная стоимость, руб", self.table_header_format)
                # worksheet.set_column("C:C", 20)
                # worksheet.write(row, 3, "Сметная стоимость, руб/м2", self.table_header_format)
                # worksheet.set_column("D:D", 20)
                worksheet.merge_range(row, 2, row, 3, "Сметная стоимость", self.table_header_format)
                worksheet.set_column("C:D", 20)
                # worksheet.write(row, 4, "Ресурсная стоимость, руб", self.table_header_format)
                # worksheet.set_column("E:E", 20)
                # worksheet.write(row, 5, "Ресурсная стоимость, руб/м2", self.table_header_format)
                # worksheet.set_column("F:F", 20)
                worksheet.merge_range(row, 4, row, 5, "Ресурсная стоимость", self.table_header_format)
                worksheet.set_column("E:F", 20)

                row += 1
                # bold = workbook.add_format({'bold': True})
                # italic = workbook.add_format({'italic': True})
                # normal = workbook.add_format()
                # cell_format.set_num_format(3)
                cell_format = workbook.add_format()
                cell_format.set_bold()
                cell_format.set_font_script(1)
                worksheet.write(row, 2, "руб", self.table_header_format)
                worksheet.write_rich_string(row, 3, "руб/м", cell_format, "2", self.table_header_format)
                worksheet.write(row, 4, "руб", self.table_header_format)
                worksheet.write_rich_string(row, 5, "руб/м", cell_format, "2", self.table_header_format)




                for element in section.get("elements"):
                    if "estimate" in element:
                        value_est = element.get("estimate").get("value")
                        value_est_per_unit = element.get("estimate").get("value_per_unit")
                    else:
                        value_est = element.get("value")
                        value_est_per_unit = element.get("value_per_unit")

                    # value = element.get("value")
                    # if value is None:
                    #     calc_type = "estimate"
                    #     if calc_type in element:
                    #         value = element.get(calc_type).get("value")
                    # # if value is not None:
                    # #     value = f'{value:,.2f}'.replace(',', ' ')
                    # value_per_unit = element.get("value_per_unit")
                    # if value_per_unit is None:
                    #     if calc_type in element:
                    #         value_per_unit = element.get(calc_type).get("value_per_unit")
                    # # if value_per_unit is not None:
                    # #     value_per_unit = f'{value_per_unit:,.2f}'.replace(',', ' ')

                    if "resource" in element:
                        value_res = element.get("resource").get("value")
                        value_res_per_unit = element.get("resource").get("value_per_unit")
                    else:
                        value_res = None
                        value_res_per_unit = None

                    row += 1
                    worksheet.write(row, 0, element.get("pos"), self.cell_left_format)
                    worksheet.write(row, 1, element.get("name"), self.cell_left_format)
                    worksheet.write(row, 2, value_est, self.number_format)
                    worksheet.write(row, 3, value_est_per_unit, self.number_format)
                    worksheet.write(row, 4, value_res, self.number_format)
                    worksheet.write(row, 5, value_res_per_unit, self.number_format)



        worksheet = workbook.add_worksheet("ОЛ"+str(id))
        sections = data.get("sections")
        row = -1
        for section in sections:
            row += 1
            worksheet.set_row(row, 30)
            worksheet.merge_range(row, 0, row, 5, section.get("name"), self.header_format)
            row += 1
            worksheet.write(row, 0, "№", self.table_header_format)
            worksheet.set_column("A:A", 10)
            worksheet.write(row, 1, "Наименование оборудования и материалов", self.table_header_format)
            worksheet.set_column("B:B", 60)
            worksheet.write(row, 2, "Единица измерения", self.table_header_format)
            worksheet.set_column("C:C", 13)
            worksheet.write(row, 3, "Количество", self.table_header_format)
            worksheet.set_column("D:D", 12)
            worksheet.write(row, 4, "Сметная стоимость", self.table_header_format)
            worksheet.set_column("E:E", 20)
            worksheet.write(row, 5, "Ресурсная стоимость", self.table_header_format)
            worksheet.set_column("F:F", 20)

            for element_type in section.get("element_types"):
                row += 1
                worksheet.write(row, 0, element_type.get("pos"), self.cell_left_bold_format)
                worksheet.write(row, 1, element_type.get("name"), self.cell_left_bold_format)
                worksheet.write(row, 2, "", self.cell_center_bold_format)
                worksheet.write(row, 3, "", self.cell_center_bold_format)
                worksheet.write(row, 4, "", self.cell_center_bold_format)
                worksheet.write(row, 5, "", self.cell_center_bold_format)
                for predict in element_type.get("predicts"):
                    row += 1
                    worksheet.write(row, 0, predict.get("pos"), self.cell_left_format)
                    worksheet.write(row, 1, predict.get("name"), self.cell_left_format)
                    worksheet.write(row, 2, predict.get("unit"), self.cell_center_format)
                    worksheet.write(row, 3, predict.get("quantity"), self.merge_format)
                    worksheet.write(row, 4, predict.get("cost_est"), self.merge_format_rub)
                    worksheet.write(row, 5, predict.get("cost"), self.merge_format_rub)
                row += 1
                worksheet.write(row, 0, "", self.cell_left_bold_format)
                worksheet.write(row, 1, "", self.cell_left_bold_format)
                worksheet.write(row, 2, "", self.cell_left_bold_format)
                worksheet.write(row, 3, "", self.cell_left_bold_format)
                worksheet.write(row, 4, "", self.cell_left_bold_format)
                worksheet.write(row, 5, "", self.cell_left_bold_format)
            row += 1
            # worksheet.write(row, 0, "", self.cell_left_bold_format)
            # worksheet.write(row, 1, "Итого по " + section.get("name"), self.cell_left_bold_format)
            # worksheet.write(row, 2, "", self.cell_left_bold_format)
            # worksheet.write(row, 3, "", self.cell_left_bold_format)
            # worksheet.write(row, 4, section.get("cost"), self.merge_format_rub)
            calc_type = "estimate"
            for key in section.get(calc_type).keys():
                row += 1
                cost = section.get(calc_type).get(key)
                worksheet.write(row, 0, "", self.cell_left_bold_format)
                worksheet.write(row, 1, cost.get("name"), self.cell_left_bold_format)
                worksheet.write(row, 2, "", self.cell_left_bold_format)
                worksheet.write(row, 3, "", self.cell_left_bold_format)
                # worksheet.write(row, 4, f'{cost.get("value"):,.2f}'.replace(',', ' '), self.merge_format_rub)
                worksheet.write(row, 4, cost.get("value"), self.merge_format_rub)
                worksheet.write(row, 5, section.get("resource").get(key).get("value"), self.merge_format_rub)
            # calc_type = "resource"
            # for key in section.get(calc_type).keys():
            #     row += 1
            #     cost = section.get(calc_type).get(key)
            #     worksheet.write(row, 0, "", self.cell_left_bold_format)
            #     worksheet.write(row, 1, cost.get("name"), self.cell_left_bold_format)
            #     worksheet.write(row, 2, "", self.cell_left_bold_format)
            #     worksheet.write(row, 3, "", self.cell_left_bold_format)
            #     # worksheet.write(row, 4, f'{cost.get("value"):,.2f}'.replace(',', ' '), self.merge_format_rub)
            #     worksheet.write(row, 4, "", self.cell_center_bold_format)
            #     worksheet.write(row, 5, cost.get("value"), self.merge_format_rub)
        # row += 1
        # worksheet.write(row, 0, "", self.cell_left_bold_format)
        # worksheet.write(row, 1, "", self.cell_left_bold_format)
        # worksheet.write(row, 2, "", self.cell_left_bold_format)
        # worksheet.write(row, 3, "", self.cell_left_bold_format)
        # worksheet.write(row, 4, "", self.cell_left_bold_format)
        # row += 1
        # worksheet.write(row, 0, "", self.cell_left_bold_format)
        # worksheet.write(row, 1, "ОБЩИЙ ИТОГ", self.cell_left_bold_format)
        # worksheet.write(row, 2, "", self.cell_left_bold_format)
        # worksheet.write(row, 3, "", self.cell_left_bold_format)
        # worksheet.write(row, 4, data.get("result").get("total_cost"), self.merge_format_rub)

        workbook.close()

        return output.getvalue()
