#!/usr/bin/env python3

"""
LocalMeet Models
@version: 2025.12
"""
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin

from localmeet import db

class Base(DeclarativeBase): ...

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)  # Google ID
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)  # Empty for OAuth users
    profile_image_path: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)

    events: Mapped[list["Event"]] = relationship(back_populates="host")
    event_registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="user")

class Event(db.Model):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    time: Mapped[datetime.time] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    cover_image_path: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    max_attendees: Mapped[int] = mapped_column(nullable=False)
    short_description: Mapped[str] = mapped_column(nullable=False)
    details: Mapped[str] = mapped_column(nullable=False)
    registration_deadline: Mapped[datetime.datetime] = mapped_column(nullable=False)
    host_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    host: Mapped["User"] = relationship(back_populates="events")
    event_registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="event", cascade="all, delete-orphan")

class EventRegistration(db.Model):
    __tablename__ = "event_registrations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="event_registrations")
    event: Mapped["Event"] = relationship(back_populates="event_registrations")
