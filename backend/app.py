from flask import Flask, request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()





def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    UPLOAD_FOLDER = "uploads/files"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    print("eveything success upto here.")
    return app

