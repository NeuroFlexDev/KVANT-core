# -*- coding: utf-8 -*-
import os

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

# Common
APP_TITLE = "OMI API"
SERVER_NAME = os.getenv("SERVER_NAME", "https://script.engineering")
SERVER_DCAPI = os.getenv("SERVER_DCAPI", "https://dcapi.dev.script.engineering")
SERVER_OMIAPI = os.getenv("SERVER_OMIAPI", "https://omimod.dev.script.engineering")

DEBUG = os.getenv("DEBUG", False)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "YCdud_(k4{(/,?oL72)r'j|7>S&=;i")

# Paths
ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
ETC_PATH = os.path.join(ROOT_PATH, "etc")
SSL_ROOT_CERT = os.getenv("SSL_ROOT_CERT", os.path.join(ETC_PATH, "root.crt"))
FPDF_FONT_DIR = os.path.join(os.path.dirname(__file__), "static", "fonts")
S3_ATTACHMENT_PATH = "omi/support/"

# Database
DEFAULT_LOCAL_DB = {
    "host": "localhost",
    "port": 5432,
    "name": "kvant_dev",
    "user": "kvant_user",
    "password": "kvant_password",
}

def _get_env_int(env_name: str, default: int) -> int:
    value = os.getenv(env_name, None)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


DB_HOST: str = os.getenv("DB_HOST", DEFAULT_LOCAL_DB["host"])
DB_USER: str = os.getenv("DB_USER", DEFAULT_LOCAL_DB["user"])
DB_PASSWORD: str = os.getenv("DB_PASSWORD", DEFAULT_LOCAL_DB["password"])
DB_PORT: int = _get_env_int("DB_PORT", DEFAULT_LOCAL_DB["port"])
DB_NAME: str = os.getenv("DB_NAME", DEFAULT_LOCAL_DB["name"])
DB_SSLMODE: str = os.getenv("DB_SSLMODE", "disable")
DB_SSLROOTCERT: str = os.getenv("DB_SSLROOTCERT", "")
DB_ECHO: bool = False

# Email
MAIL_HOST = os.getenv("MAIL_HOST", "smtp.yandex.ru")
MAIL_PORT = os.getenv("MAIL_PORT", 587)
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", True)
MAIL_HOST_USER = os.getenv("MAIL_HOST_USER", "account@script.engineering")
MAIL_HOST_PASSWORD = os.getenv("MAIL_HOST_PASSWORD", "vxigfaoakgptjsup")
MAIL_FROM = os.getenv("MAIL_FROM", "account@script.engineering")
# MAIL_SUPPORT = os.getenv("MAIL_SUPPORT", "markovkm@script.engineering")
MAIL_SUPPORT = os.getenv("MAIL_SUPPORT", "account@script.engineering")


CONFIRM_TIMEOUT = 10  # время подтверждения операций восстановления пароля и смены адреса электронной почты в минутах
MAIL_TIMEOUT = os.getenv("MAIL_TIMEOUT", 10)
MAIL_DEBUG_RECIPIENTS = [
    # "sergelab@gmail.com",
    # "ae.fronttier@script.engineering",
    # "yl.fronttier@script.engineering",
]  # Можно добавить еще

# Sentry
SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
SENTRY_ENV: str = os.getenv("SENTRY_ENV", "")

# Templates
TEMPLATES_FOLDER: str = os.path.join(os.path.dirname(__file__), "templates")

# Apis
API_ROUTES = ["auth", "users", "directories", "registry", "services", "logs", "questionnaire"]

if os.path.isfile(os.path.join(os.path.dirname(__file__), "settings_local.py")):
    from settings_local import *  # nopycln: import

# s3
AWS_KEY_ID = os.getenv("AWS_KEY_ID", "")
AWS_SECRET = os.getenv("AWS_SECRET", "")
AWS_BUCKET = os.getenv("AWS_BUCKET", "")

# Sentry
sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=SENTRY_ENV,
    send_default_pii=True,
    attach_stacktrace=True,
    integrations=[FastApiIntegration(), SqlalchemyIntegration()],
    traces_sample_rate=1.0,
)

# default_calc_params (по справочнику Минстроя)
DEFAULT_REGION = "г. Москва"
DEFAULT_PERIOD_1 = "2023-3"
DEFAULT_PERIOD_2 = "2025-1"
