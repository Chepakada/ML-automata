from flask import Flask
import os
from extensions import db, migrate, ma, cors, make_celery

def create_app():
    app = Flask(__name__)
    UPLOAD_FOLDER = "uploads/files"
    DOWNLOAD_FOLDER = "downloads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CELERY_BROKER_URL"] = 'redis://127.0.0.1:6379/0'
    app.config["CELERY_RESULT_BACKEND"] = 'redis://127.0.0.1:6379/0'
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    celery = make_celery(app)

    # with app.app_context():
    from app.routes import bp as main_bp  # Ensure correct import path
    app.register_blueprint(main_bp)  # Ensure correct URL prefix

    return app, celery
