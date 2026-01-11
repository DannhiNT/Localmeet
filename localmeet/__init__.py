#!/usr/bin/env python3

"""
LocalMeet Initialization
@version: 2025.12
"""

import pathlib
import secrets

import dotenv
import requests
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from oauthlib.oauth2 import WebApplicationClient

db = SQLAlchemy()
mm = Marshmallow()
client = WebApplicationClient("")

def create_app() -> Flask:
    from localmeet.routes.event_routes import event_bp
    from localmeet.routes.user_routes import user_bp
    from localmeet.auth import auth_bp, login_manager

    this_app = Flask(__name__)
    this_dir = pathlib.Path(__file__).parent
    dotenv.load_dotenv(this_dir / pathlib.Path(".flaskenv"))
    this_app.config.from_prefixed_env()
    
    env_file = this_dir.parent / pathlib.Path(".env")
    if env_file.exists():
        this_app.config.from_mapping(dotenv.dotenv_values(env_file))
    
    data_file = this_app.config.get("DATA_FILE", "local-meet")
    db_file = this_dir.parent / f"{data_file}.sqlite3"

    this_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file}"

    if not this_app.config.get("SECRET_KEY"):
        this_app.config["SECRET_KEY"] = secrets.token_hex()

    if this_app.config.get("GOOGLE_CLIENT_ID"):
        with this_app.app_context():
            client.client_id = this_app.config["GOOGLE_CLIENT_ID"]
        GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
        this_app.config["GOOGLE_CONFIG"] = requests.get(GOOGLE_DISCOVERY_URL).json()
    else:
        this_app.config["GOOGLE_CONFIG"] = {}

    db.init_app(this_app)

    login_manager.init_app(this_app)
    login_manager.login_view = "auth.login"
    
    with this_app.app_context():
        db.create_all()
    with this_app.app_context():
        mm.init_app(this_app)
    
    this_app.register_blueprint(event_bp)
    this_app.register_blueprint(user_bp)
    this_app.register_blueprint(auth_bp)

    return this_app