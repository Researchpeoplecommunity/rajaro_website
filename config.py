import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEV_SECRET_KEY = "rajaro-dev-secret-change-in-production"
DEV_ADMIN_PASSWORD = "admin123"


def is_production():
    return (
        os.environ.get("RENDER") == "true"
        or os.environ.get("FLASK_ENV") == "production"
    )


def database_url():
    url = os.environ.get("DATABASE_URL")
    if url:
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url
    return f"sqlite:///{BASE_DIR / 'rajaro.db'}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", DEV_SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = (
        {"pool_pre_ping": True, "pool_recycle": 300}
        if database_url().startswith("postgresql")
        else {}
    )

    DEBUG = os.environ.get("FLASK_DEBUG") == "1" and not is_production()
    TESTING = False

    LOGIN_DISABLED = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = is_production()

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", DEV_ADMIN_PASSWORD)

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", str(BASE_DIR / "static" / "uploads"))
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 8 * 1024 * 1024))


def validate_production_config():
    if not is_production():
        return
    if Config.SECRET_KEY == DEV_SECRET_KEY:
        raise RuntimeError("SECRET_KEY must be set in production.")
    if Config.ADMIN_PASSWORD == DEV_ADMIN_PASSWORD:
        raise RuntimeError("ADMIN_PASSWORD must be changed in production.")
