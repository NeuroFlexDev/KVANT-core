"""
Заглушка для StorageHandler
"""
from handlers import BaseHandler
from typing import List, Optional
from fastapi import UploadFile
from dc_core.models.requests import CreateStatementRequest, UpdateStatementRequest
from dc_core.models.responses import StatementResponse, AttachmentResponse


class StorageHandler(BaseHandler):
    """Заглушка для обработки хранилища"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save_file(self, file_data: bytes, filename: str):
        """Заглушка для сохранения файла"""
        return {"success": True, "filename": filename, "size": len(file_data)}

    def get_file(self, filename: str):
        """Заглушка для получения файла"""
        return {"success": True, "filename": filename, "data": b"mock_file_data"}

    def uploadfile(self, statement_guid: str, files: List[UploadFile], current_user):
        """Заглушка для загрузки файлов"""
        return {"success": True, "uploaded_count": len(files)}

    def downloadfile(self, guid: str):
        """Заглушка для скачивания файла"""
        return {"success": True, "guid": guid}

    def deletefile(self, filename: str):
        """Заглушка для удаления файла"""
        return {"success": True, "filename": filename}

    def uploaded_list(self, path: Optional[str] = None):
        """Заглушка для списка загруженных файлов"""
        return {"files": []}

    def get_statements(self, id: Optional[int] = None, state_id: Optional[int] = None, current_user=None):
        """Заглушка для получения заявлений"""
        return [StatementResponse(id=1, title="Test Statement", description="Test Description")]

    def create_statement(self, data: CreateStatementRequest, current_user):
        """Заглушка для создания заявления"""
        return StatementResponse(id=1, title=data.title, description=data.description)

    def update_statement(self, data: UpdateStatementRequest, current_user):
        """Заглушка для обновления заявления"""
        return StatementResponse(id=data.id, title=data.title, description=data.description)

    def delete_statement(self, id: int, current_user):
        """Заглушка для удаления заявления"""
        return StatementResponse(id=id, title="Deleted", description="Deleted")

    def get_attachments_by_statement_guid(self, statement_guid: str, current_user):
        """Заглушка для получения вложений по GUID заявления"""
        return [AttachmentResponse(id=1, filename="test.pdf", size=1024)]

    def delete_attachment(self, guid: str, current_user):
        """Заглушка для удаления вложения"""
        return AttachmentResponse(id=1, filename="deleted.pdf", size=0)