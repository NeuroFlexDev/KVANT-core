from . import BaseHandler
import urllib.parse
import os
from fastapi import HTTPException, UploadFile
from ..coreutils.smtp import EMailMessage, send_email, EMailAttachment
from typing import List, Optional
from dc_core.services.s3 import S3
from starlette.responses import Response
from ..models.db.user import DBUser
from datetime import datetime

from dc_core.models.requests import (
    CreateStatementRequest,
    UpdateStatementRequest,
    CreateAttachmentRequest,
)

from dc_core.models.responses import (
    StatementResponse,
    AttachmentResponse,
)


__all__ = ("StorageHandler",)


class StorageHandler(BaseHandler):
    def uploadfile(self, statement_guid: str, files: List[UploadFile], current_user: DBUser, **kwargs):

        path = os.path.join(self.settings.S3_ATTACHMENT_PATH, str(datetime.now().year))
        statement = self.db_layer.storage.get_statement_by_guid(guid=statement_guid)
        file_names = []

        for file in files:
            if file.content_type not in ["application/pdf",
                                         "image/png",
                                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                raise HTTPException(403, detail=f"Недопустимый формат файла {file.filename}. Разрешенный форматы: .pdf,.png,.docx")

            file_size = file.size
            if file_size > 3 * 1024 * 1024:
                raise HTTPException(403, detail=f"Файл {file.filename} превышает максимально допустимый размер 3 Мб")

            data = {
                # "user_id": current_user.id,
                "path_to_object": path,
                "statement_id": statement.get("id"),
                "file_name": file.filename,
                # "file_extension": file.filename.rsplit('.', 1)[1].lower(),
                "content_type": file.content_type
            }
            attachment = self.create_attachment(CreateAttachmentRequest(**data), current_user)
            file_names.append(attachment.guid)

        body = S3().uploadfile(path, files, file_names, self.settings.AWS_KEY_ID, self.settings.AWS_SECRET, self.settings.AWS_BUCKET)

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return

    def downloadfile(self, guid: str, **kwargs):
        attachment = self.db_layer.storage.get_attachment_by_guid(guid=guid)
        filename = os.path.join(attachment.get("path_to_object"), attachment.get("guid")).replace("\\", "/")
        filename_out = attachment.get("file_name")
        media_type = attachment.get("content_type")

        body = S3().downloadfile(filename, self.settings.AWS_KEY_ID, self.settings.AWS_SECRET, self.settings.AWS_BUCKET)

        return Response(
            body,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={urllib.parse.quote(filename_out)}"},
        )

    def deletefile(self, filename: Optional[str] = None, **kwargs):
        if filename is None:
            raise HTTPException(404, "Необходимо указать имя файла")
        body = S3().deletefile(filename, self.settings.AWS_KEY_ID, self.settings.AWS_SECRET, self.settings.AWS_BUCKET)
        return body

    def uploaded_list(self, path: str, **kwargs):
        if path:
            path = path.strip()
            if path[len(path) - 1] != "/":
                path = path + "/"
        try:
            list = S3().uploaded_list(path, self.settings.AWS_KEY_ID, self.settings.AWS_SECRET, self.settings.AWS_BUCKET)
        except Exception as e:
            raise HTTPException(404, "Каталог не найден")
        return list


    def get_statements(self, id: int, state_id: int, current_user: DBUser) -> List[StatementResponse]:
        if id:
            rs = self.db_layer.storage.get_statement_by_id(id=id, user_id=current_user.id)
        else:
            rs = self.db_layer.storage.get_statements(state_id=state_id, user_id=current_user.id)
        return [StatementResponse(**r) for r in rs] if rs else []

    def create_statement(self, data: CreateStatementRequest, current_user: DBUser) -> StatementResponse:
        statement = self.db_layer.storage.create_statement(statementtype_id=data.statementtype_id, user_id=current_user.id)

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return StatementResponse(**statement)

    def update_statement(self, data: UpdateStatementRequest, current_user: DBUser) -> StatementResponse:
        rs = self.db_layer.storage.update_statement(user_id=current_user.id, **data.dict())

        if not rs:
            raise HTTPException(404, f"Обращение с ID={data.id} не найдено")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e
        else:
            attachments = self.get_attachments_by_statement_guid(rs.get("guid"), current_user)
            content = []
            for attachment in attachments:
                filename = attachment.path_to_object + '/' + attachment.guid
                body = S3().downloadfile(filename,
                                         self.settings.AWS_KEY_ID,
                                         self.settings.AWS_SECRET,
                                         self.settings.AWS_BUCKET
                                         )
                content.append(
                    EMailAttachment(
                        filename=attachment.file_name, #base64.b64encode(attachment.file_name.encode("UTF-8")),
                        content=body,
                        mime=attachment.content_type
                    )
                )

            context = {
                "datetime": rs.get("modifydate").strftime("%d.%m.%Y %H:%M:%S"),
                "email": current_user.email,
                "statement_type": rs.get("statementtype_name"),
                "statement_topic": rs.get("topic"),
                "statement_body": rs.get("body"),
            }
            self.add_task(
                send_email,
                EMailMessage(
                    to_addrs=[self.settings.MAIL_SUPPORT],
                    subject="Обращение в техподдержку системы SCRIPT ENGINEERING",
                    body=self.templates.get_template("email/support.txt").render(context),
                    # body_html=self.templates.get_template("email/support.html").render(context).replace("\n","<br />\n"),
                    attachments=content
                ),
            )

        return StatementResponse(**rs)

    def delete_statement(self, id: int, current_user: DBUser) -> StatementResponse:
        rs = self.db_layer.storage.delete_statement(id=id, user_id=current_user.id)

        if not rs:
            raise HTTPException(404, f"Обращение с ID={id} не найдено")

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return rs


    def get_attachments_by_statement_guid(self, statement_guid: str, current_user: DBUser) -> List[AttachmentResponse]:
        rs = self.db_layer.storage.get_attachments_by_statement_guid(statement_guid=statement_guid, user_id=current_user.id)
        return [AttachmentResponse(**r) for r in rs] if rs else []

    def create_attachment(self, data: CreateAttachmentRequest, current_user: DBUser) -> AttachmentResponse:
        attachment = self.db_layer.storage.create_attachment(user_id=current_user.id, **data.dict())
        return AttachmentResponse(**attachment)

    def delete_attachment(self, guid: str, current_user: DBUser) -> AttachmentResponse:
        rs = self.db_layer.storage.delete_attachment(guid=guid, user_id=current_user.id)
        if not rs:
            raise HTTPException(404, "Файл не найден")

        # удалить файлы из хранилища s3
        # filename = os.path.join(rs.get("path_to_object"), rs.get("guid")).replace("\\", "/")
        # body = S3().deletefile(filename, self.settings.AWS_KEY_ID, self.settings.AWS_SECRET, self.settings.AWS_BUCKET)

        try:
            self.db_layer.commit()
        except Exception as e:
            self.db_layer.rollback()
            raise e

        return AttachmentResponse(**rs)