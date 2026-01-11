#!/usr/bin/env python3

"""
LocalMeet Event Routes
@version: 2025.12
"""
import json
import os
from datetime import datetime, time
from localmeet import db
from localmeet.models import User, Event, EventRegistration
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from flask import current_app

event_bp = Blueprint("events", __name__, url_prefix="/events")

@event_bp.get("/")
def event_list():
    events = db.session.query(Event).all()
    return render_template("event_list.jinja", events=events)

@event_bp.get("/<int:event_id>")
def event_detail(event_id):
    event = db.session.query(Event).filter_by(id=event_id).first()
    if not event:
      return render_template("error.jinja", code=404, message="Sorry, we couldn’t find the page you were looking for."), 404
    
    current_registrations = len(event.event_registrations)
    is_full = current_registrations >= event.max_attendees
    event_details = json.loads(event.details)  # Get details stored as JSON string

    # Check if current user is registered for the event
    user_registered = False
    if current_user.is_authenticated:
        user_registered = EventRegistration.query.filter_by(
            user_id=current_user.id,
            event_id=event.id
        ).first() is not None
    # Fetch attendees registered for the event
    event_registered_users = db.session.query(User).join(EventRegistration).filter(EventRegistration.event_id == event.id).all()

    return render_template("show.jinja", 
                            event=event, 
                            current_registrations=current_registrations, 
                            is_full=is_full, 
                            event_details=event_details, 
                            user_registered=user_registered,
                            event_registered_users=event_registered_users)
    

@event_bp.get("/new")
@login_required
def new_event_form():
    return render_template("event_form.jinja", form_action=url_for("events.create_event"))

@event_bp.post("/new")
@login_required
def create_event():
    title = request.form.get("title")
    date_str = request.form.get("date")
    time_str = request.form.get("time")
    location = request.form.get("location")

    cover_image = request.files.get("cover_image")
    save_path = os.path.join(current_app.root_path, "static/uploads", cover_image.filename)
    cover_image.save(save_path)
    cover_image_path = f"/static/uploads/{cover_image.filename}"

    price = float(request.form.get("price", 0))
    max_attendees = int(request.form.get("max_attendees", 0))
    short_description = request.form.get("short_description")
    details = request.form.get("details")
    registration_deadline_str = request.form.get("registration_deadline")

    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    time = datetime.strptime(time_str, "%H:%M").time()
    registration_deadline = datetime.strptime(registration_deadline_str, "%Y-%m-%dT%H:%M")

    new_event = Event(
        title=title,
        date=date,
        time=time,
        location=location,
        cover_image_path=cover_image_path,
        price=price,
        max_attendees=max_attendees,
        short_description=short_description,
        details=details,
        registration_deadline=registration_deadline,
        host_id=current_user.id
    )
    db.session.add(new_event)
    db.session.commit()

    flash("Successfully create new event.", "success")
    return redirect(url_for("events.event_list"))

@event_bp.route("/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
  event = db.session.query(Event).filter_by(id=event_id).first()
  
  if not event:
    return render_template("error.jinja", code=404, message="Sorry, we couldn’t find the page you were looking for."), 404
  
  if event.host_id != current_user.id: 
    return render_template("error.jinja", code=403, message="You do not have permission to edit this event."), 403

  if request.method == "GET":
    event_details = json.loads(event.details) # Get event details as dictionary and pass to template
    return render_template("event_form.jinja", form_action=url_for("events.edit_event", event_id=event.id), event=event, event_details=event_details)
  else:  # POST (update)
    event.title = request.form.get("title")
    date_str = request.form.get("date")
    time_str = request.form.get("time")
    event.location = request.form.get("location")

    cover_image = request.files.get("cover_image")
    if cover_image:
      save_path = os.path.join(current_app.root_path, "static/uploads", cover_image.filename)
      cover_image.save(save_path)
      event.cover_image_path = f"/static/uploads/{cover_image.filename}"

    event.price = float(request.form.get("price", 0))
    event.max_attendees = int(request.form.get("max_attendees", 0))
    event.short_description = request.form.get("short_description")
    event.details = request.form.get("details")
    registration_deadline_str = request.form.get("registration_deadline")

    event.date = datetime.strptime(date_str, "%Y-%m-%d").date()
    event.time = datetime.strptime(time_str, "%H:%M:%S").time()
    event.registration_deadline = datetime.strptime(registration_deadline_str, "%Y-%m-%dT%H:%M")

    db.session.commit()

    flash("Successfully update event.", "success")
    return redirect(url_for("events.event_list", event_id=event.id))

@event_bp.post("/delete/<int:event_id>")
@login_required
def delete_event(event_id):
    event = db.session.query(Event).filter_by(id=event_id).first()

    if event.host_id != current_user.id:
      return render_template("error.jinja", code=403, message="You do not have permission to delete this event."), 403

    if not event:
      return render_template("error.jinja", code=404, message="Sorry, we could not delete a nonexisting event"), 404

    db.session.delete(event)
    db.session.commit()
    flash("Successfully delete event.", "success")
    return redirect(url_for("events.event_list"))

# Event Registrations
@event_bp.post("/register/<int:event_id>")
@login_required
def register_for_event(event_id):
    event = db.session.query(Event).filter_by(id=event_id).first()

    if not event:
      return render_template("error.jinja", code=404, message="Sorry, we could not find the page you were looking for."), 404

    existing_registration = db.session.query(EventRegistration).filter_by(user_id=current_user.id, event_id=event_id).first()
    if existing_registration:
      return render_template("error.jinja", code=400, message="You are already registered for this event."), 400
    new_registration = EventRegistration(
        user_id=current_user.id,
        event_id=event_id
    )
    db.session.add(new_registration)
    db.session.commit()
    flash("Successfully register to join!", "success")
    return redirect(url_for("events.event_detail", event_id=event_id))

@event_bp.post("/deregister/<int:event_id>")
@login_required
def deregister_from_event(event_id):
    try:
        registration = db.session.query(EventRegistration).filter_by(
            user_id=current_user.id, event_id=event_id
        ).first()

        if not registration:
            flash("You are not registered for this event.", "warning")
            return redirect(url_for("events.event_list"))

        db.session.delete(registration)
        db.session.commit()

        flash("Successfully cancelled registration.", "success")
        return redirect(url_for("events.event_list"))
    
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while cancelling registration: {str(e)}", "danger")
        return redirect(url_for("events.event_list")) 