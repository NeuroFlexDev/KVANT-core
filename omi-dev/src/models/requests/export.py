from enum import Enum, unique

@unique
class ReportFormat(str, Enum):
    PDF = "pdf"
    EXCEL = "xlsx"
    WORD = "docx"
