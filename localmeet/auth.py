#!/usr:bin/env python3

"""
LocalMeet authentication with Google OAuth
@version: 2025.12
"""

import datetime
import json

import requests
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from localmeet import db, client
from localmeet.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in to access this page.", "warning")
    return redirect(url_for("auth.login"))

@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("events.event_list"))
    
    if not current_app.config.get("GOOGLE_CLIENT_ID"):
        return "OAuth not configured.", 500

    google_provider_cfg = current_app.config["GOOGLE_CONFIG"]
    authorization_endpoint = google_provider_cfg.get("authorization_endpoint")
    
    if not authorization_endpoint:
        return "OAuth configuration error.", 500
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("auth.callback", _external=True),
        scope=["openid", "email", "profile"],
    )
    
    return redirect(request_uri)

@auth_bp.route("/login/callback")
def callback():
    code = request.args.get("code")
    
    google_provider_cfg = current_app.config["GOOGLE_CONFIG"]
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config["GOOGLE_CLIENT_ID"], current_app.config["GOOGLE_CLIENT_SECRET"]),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    userinfo = userinfo_response.json()
    if userinfo.get("email_verified"):
        google_id = userinfo["sub"]
        email = userinfo["email"]
        picture = userinfo.get("picture", "")
        given_name = userinfo.get("given_name", "")
        family_name = userinfo.get("family_name", "")
    else:
        return "User email not available or not verified by Google.", 400
    
    user = db.session.query(User).filter_by(id=google_id).first()
    
    if not user:
        user = User(
            id=google_id,
            email=email,
            first_name=given_name,
            last_name=family_name,
            password_hash="",
            profile_image_path=picture
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash(f"Welcome, {user.first_name}!", "success")
    
    return redirect(url_for("events.event_list"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))