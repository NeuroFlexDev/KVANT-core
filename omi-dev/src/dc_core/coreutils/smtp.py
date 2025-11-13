# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import os


__all__ = ("EMailMessage", "EMailAttachment", "send_email")


class EMailAttachment:
    """Email attachment class"""

    def __init__(self, filename: str, content: bytes, content_type: str = "application/octet-stream"):
        self.filename = filename
        self.content = content
        self.content_type = content_type


class EMailMessage:
    """Email message class"""

    def __init__(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: str = None,
        attachments: List[EMailAttachment] = None,
        html_body: str = None
    ):
        self.to_email = to_email
        self.subject = subject
        self.body = body
        self.from_email = from_email or os.getenv("MAIL_FROM_ADDRESS", "noreply@example.com")
        self.attachments = attachments or []
        self.html_body = html_body


def send_email(message: EMailMessage) -> bool:
    """Send email message"""
    try:
        # Get SMTP settings from environment
        smtp_host = os.getenv("MAIL_HOST", "smtp.yandex.ru")
        smtp_port = int(os.getenv("MAIL_PORT", "587"))
        smtp_user = os.getenv("MAIL_HOST_USER", "")
        smtp_password = os.getenv("MAIL_HOST_PASSWORD", "")

        if not smtp_user or not smtp_password:
            print(f"SMTP credentials not configured. Would send email to {message.to_email} with subject: {message.subject}")
            return True

        # Create message
        msg = MIMEMultipart()
        msg['From'] = message.from_email
        msg['To'] = message.to_email
        msg['Subject'] = message.subject

        # Add body
        if message.html_body:
            msg.attach(MIMEText(message.html_body, 'html'))
        else:
            msg.attach(MIMEText(message.body, 'plain'))

        # Add attachments
        for attachment in message.attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.content)
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {attachment.filename}'
            )
            msg.attach(part)

        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False