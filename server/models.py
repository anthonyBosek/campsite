from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class TimestampMixin:
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_onupdate=db.func.now())


class Park(db.Model, SerializerMixin, TimestampMixin):
    __tablename__ = "parks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    entrance_fee = db.Column(db.Float)
    has_trails = db.Column(db.Boolean)
    has_RV_cleanout = db.Column(db.Boolean)
    begin_camping_season = db.Column(db.DateTime)
    end_camping_season = db.Column(db.DateTime)

    reservations = db.relationship(
        "Reservation", back_populates="park", cascade="all, delete-orphan"
    )
    campsites = association_proxy("reservations", "campsite")

    serialize_rules = ("-reservations.park", "-campsites.parks")

    # validations

    def __repr__(self):
        return f"<Park #{self.id} >"


class Campsite(db.Model, SerializerMixin, TimestampMixin):
    __tablename__ = "campsites"

    id = db.Column(db.Integer, primary_key=True)
    park_name = db.Column(db.String)
    max_capacity = db.Column(db.Integer)
    type = db.Column(db.String)
    site_fee = db.Column(db.Float)
    has_water = db.Column(db.Boolean)
    has_bathroom = db.Column(db.Boolean)
    has_grill = db.Column(db.Boolean)

    # relationships
    reservations = db.relationship(
        "Reservation", back_populates="campsite", cascade="all, delete-orphan"
    )
    parks = association_proxy("reservations", "park")

    serialize_rules = ("-reservations.campsite", "-parks.campsites")

    # validations

    def __repr__(self):
        return f"<Campsite #{self.id} >"


class Reservation(db.Model, SerializerMixin, TimestampMixin):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    camper = db.Column(db.String)
    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))
    campsite_id = db.Column(db.Integer, db.ForeignKey("campsites.id"))

    park = db.relationship("Park", back_populates="reservations")
    campsite = db.relationship("Campsite", back_populates="reservations")

    serialize_rules = ("-park.reservations", "-campsite.reservations")

    # validations

    def __repr__(self):
        return f"<Reservation #{self.id} >"
