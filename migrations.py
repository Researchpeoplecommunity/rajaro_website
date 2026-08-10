"""Lightweight schema migrations for SQLite/PostgreSQL without Alembic."""

from sqlalchemy import inspect, text

from models import db


def _has_column(table, column):
    inspector = inspect(db.engine)
    if table not in inspector.get_table_names():
        return False
    return column in {col["name"] for col in inspector.get_columns(table)}


def _add_column(table, column, col_type):
    if _has_column(table, column):
        return
    db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
    db.session.commit()


def migrate_schema():
    db.create_all()

    _add_column("service_category", "service_group", "VARCHAR(40) DEFAULT 'technology'")
    _add_column("service_item", "is_active", "BOOLEAN DEFAULT 1")
    _add_column("product", "image_filename", "VARCHAR(300)")
    _add_column("product", "short_description", "TEXT")
    _add_column("learning_service", "image_filename", "VARCHAR(300)")
    _add_column("learning_service", "cta_url", "VARCHAR(300)")
    _add_column("learning_service", "cta_text", "VARCHAR(80) DEFAULT 'Learn More'")
    _add_column("learning_service", "is_active", "BOOLEAN DEFAULT 1")
    _add_column("blog_post", "featured_image", "VARCHAR(300)")
    _add_column("blog_post", "sort_order", "INTEGER DEFAULT 0")
    _add_column("why_choose_item", "is_active", "BOOLEAN DEFAULT 1")
    _add_column("why_choose_item", "sort_order", "INTEGER DEFAULT 0")

    db.create_all()
