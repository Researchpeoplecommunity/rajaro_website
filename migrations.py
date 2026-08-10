"""Lightweight schema migrations for SQLite/PostgreSQL without Alembic."""

from sqlalchemy import inspect, text

from models import db  # noqa: F401 — registers all models on metadata


def _dialect():
    return db.engine.dialect.name


def _bool_default():
    return "TRUE" if _dialect() == "postgresql" else "1"


def _has_column(table, column):
    inspector = inspect(db.engine)
    if table not in inspector.get_table_names():
        return False
    return column in {col["name"] for col in inspector.get_columns(table)}


def _has_table(table):
    inspector = inspect(db.engine)
    return table in inspector.get_table_names()


def _add_column(table, column, col_type):
    if not _has_table(table) or _has_column(table, column):
        return
    try:
        db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
        db.session.commit()
    except Exception:
        db.session.rollback()
        if not _has_column(table, column):
            raise


def _widen_column(table, column, col_type):
    """Alter column type (PostgreSQL/SQLite)."""
    if not _has_table(table) or not _has_column(table, column):
        return
    if _dialect() == "postgresql":
        sql = f"ALTER TABLE {table} ALTER COLUMN {column} TYPE {col_type}"
    else:
        sql = f"ALTER TABLE {table} ALTER COLUMN {column} {col_type}"
    try:
        db.session.execute(text(sql))
        db.session.commit()
    except Exception:
        db.session.rollback()


def migrate_schema():
    db.create_all()

    bool_def = _bool_default()

    _add_column("service_category", "service_group", "VARCHAR(40) DEFAULT 'technology'")
    _add_column("service_item", "is_active", f"BOOLEAN DEFAULT {bool_def}")
    _add_column("product", "image_filename", "VARCHAR(300)")
    _add_column("product", "short_description", "TEXT")
    _add_column("learning_service", "image_filename", "VARCHAR(300)")
    _add_column("learning_service", "cta_url", "VARCHAR(300)")
    _add_column("learning_service", "cta_text", "VARCHAR(80) DEFAULT 'Learn More'")
    _add_column("learning_service", "is_active", f"BOOLEAN DEFAULT {bool_def}")
    _add_column("blog_post", "featured_image", "VARCHAR(300)")
    _add_column("blog_post", "sort_order", "INTEGER DEFAULT 0")
    _add_column("why_choose_item", "is_active", f"BOOLEAN DEFAULT {bool_def}")
    _add_column("why_choose_item", "sort_order", "INTEGER DEFAULT 0")

    # Wider field for multi-select product/service labels from contact/consultation forms
    _widen_column("consultation_booking", "service_interest", "TEXT")
    _widen_column("contact_submission", "looking_for", "TEXT")

    db.create_all()
