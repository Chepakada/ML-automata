from flask import Flask, request
import os
from extensions import db, migrate, ma, cors, make_celery
import redis

app = Flask(__name__)



def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    UPLOAD_FOLDER = "uploads/files"
    DOWNLOAD_FOLDER = "downloads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CELERY_BROKER_URL"] =    'redis://127.0.0.1:6379/0',
    app.config["CELERY_RESULT_BACKEND"] = 'redis://127.0.0.1:6379/0'
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    print("eveything success upto here.")
    

    
        
    
    celery = make_celery(app)
    
    with app.app_context():
        from routes import bp as main_bp
        app.register_blueprint(main_bp)
    

    return app, celery

app, celery = create_app()


