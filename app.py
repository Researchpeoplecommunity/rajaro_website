import os

from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config, validate_production_config
from models import AdminUser, db
from routes_admin import admin_bp
import routes_admin_cms  # noqa: F401 — registers extended CMS routes
from routes_public import public_bp
from migrations import migrate_schema
from seed import patch_database, seed_database


def create_app():
    validate_production_config()

    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    if Config.SESSION_COOKIE_SECURE or os.environ.get("BEHIND_PROXY") == "1":
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "admin.login"
    login_manager.login_message = "Please log in to access the admin panel."
    login_manager.login_message_category = "error"
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(AdminUser, int(user_id))
        except (TypeError, ValueError):
            return None

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        migrate_schema()
        if not AdminUser.query.first():
            admin = AdminUser(username=Config.ADMIN_USERNAME)
            admin.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
        seed_database()
        patch_database()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, port=int(os.environ.get("PORT", 5000)))
