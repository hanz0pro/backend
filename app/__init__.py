from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from app.services.jwt_global_error_handler import register_jwt_error_handlers

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
        minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', 15))
    )
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(
        days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 30))
    )
    CORS(app, origins=["http://localhost:5173"])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    register_jwt_error_handlers(app)



    from .routes import api
    from .routes import game_bp
    from app.routes.game_genre_routes import genre_bp
    from app.routes.game_tag_routes import tag_bp
    from app.services.global_error_handler import error_bp

    app.register_blueprint(error_bp)
    app.register_blueprint(genre_bp, url_prefix='/genre')
    app.register_blueprint(tag_bp, url_prefix='/tag')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(game_bp, url_prefix='/games')
    return app
