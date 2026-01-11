#!/usr/bin/env python3

"""
LocalMeet User Routes
@version: 2025.12
"""
import os
from datetime import datetime
from localmeet import db
from localmeet.models import User, Event, EventRegistration
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from flask import current_app

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.get("/profile/<user_id>")
def user_profile(user_id):
  user = db.session.query(User).filter_by(id=user_id).first_or_404()
  return render_template("user_profile.jinja", user=user)

@user_bp.get("/profile/edit/<user_id>")
def get_user_profile_form(user_id):
    user = db.session.query(User).filter_by(id=user_id).first_or_404()
    return render_template("user_profile_form.jinja", user=user)

@user_bp.post("/profile/edit/<user_id>")
def edit_user_profile(user_id):
    user = db.session.query(User).filter_by(id=user_id).first_or_404()
    
    user.first_name = request.form.get("first_name", user.first_name)
    user.last_name = request.form.get("last_name", user.last_name)
    user.phone_number = request.form.get("phone_number", user.phone_number)
    user.location = request.form.get("location", user.location)
    user.bio = request.form.get("bio", user.bio)

    profile_image = request.files.get("profile_image")
    if profile_image:
        image_path = os.path.join(current_app.root_path, "static/user_profile_images", profile_image.filename)
        profile_image.save(image_path)
        user.profile_image_path = f"/static/user_profile_images/{profile_image.filename}"

    db.session.commit()
    flash("Profile updated successfully!", "success")
    return redirect(url_for("user.user_profile", user_id=user.id))

@user_bp.get("/registered_events")
@login_required
def registered_event_list():
    existing_registrations = db.session.query(EventRegistration).filter_by(
        user_id=current_user.id).all()
    
    events = [registration.event for registration in existing_registrations]
    return render_template("event_list.jinja", events=events)


@user_bp.get("/posted_events")
@login_required
def posted_event_list():
    posted_events = db.session.query(Event).filter_by(
        host_id=current_user.id).all()
    
    return render_template("event_list.jinja", events=posted_events)