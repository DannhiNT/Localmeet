#!/usr/bin/env python3

"""
LocalMeet schemas

@version: 2025.12
"""

from marshmallow import fields
from localmeet import mm
from localmeet.models import Event, EventRegistration, User

class UserSchema(mm.SQLAlchemyAutoSchema):
  class Meta:
    model: User
    load_instance = True
  
  events = fields.Nested("EventSchema", many=True, exclude=["host"])
  event_registrations = fields.Nested("EventRegistrationSchema", many=True, exclude=["user"])

class EventSchema(mm.SQLAlchemyAutoSchema):
  class Meta:
    model: Event
    load_instance = True
  
  host = fields.Nested("UserSchema", exclude=["events", "event_registrations"])
  event_registrations = fields.Nested("EventRegistrationSchema", many=True, exclude=["event"])

class EventRegistrationSchema(mm.SQLAlchemyAutoSchema):
  class Meta:
    model: EventRegistration
    load_instance = True
  
  user = fields.Nested("UserSchema", exclude=["events", "event_registrations"])
  event = fields.Nested("EventSchema", exclude=["host", "event_registrations"])