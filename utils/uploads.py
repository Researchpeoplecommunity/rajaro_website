import os
import uuid

from werkzeug.utils import secure_filename

IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx"}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | DOCUMENT_EXTENSIONS


def upload_folder():
    from flask import current_app
    return current_app.config["UPLOAD_FOLDER"]


def allowed_file(filename, extensions=None):
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    allowed = extensions or ALLOWED_EXTENSIONS
    return ext in allowed


def save_document(file, prefix="doc", extensions=None):
    exts = extensions or {"pdf"}
    return save_upload(file, prefix=prefix, extensions=exts)


def save_upload(file, prefix="media", extensions=None):
    exts = extensions or ALLOWED_EXTENSIONS
    if not file or not file.filename or not allowed_file(file.filename, exts):
        return None
    folder = upload_folder()
    os.makedirs(folder, exist_ok=True)
    original = secure_filename(file.filename)
    name = f"{prefix}_{uuid.uuid4().hex[:12]}_{original}"
    file.save(os.path.join(folder, name))
    return name


def upload_url(filename):
    if not filename:
        return None
    from flask import url_for
    return url_for("public.uploaded_file", filename=filename)
