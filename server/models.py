from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

MIN_FEE = 13.99
MAX_FEE = 25
MAX_CAPACITY = 10
SITE_TYPES = ("tent", "RV")


class Park(db.Model, SerializerMixin):
    __tablename__ = "parks"

    serialize_rules = ("-campsites.park", "-created_at", "-updated_at")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String, nullable=False)
    entrance_fee = db.Column(db.Float)
    has_trails = db.Column(db.Boolean)
    has_RV_cleanout = db.Column(db.Boolean)
    begin_camping_season = db.Column(db.DateTime)
    end_camping_season = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    campsites = db.relationship("Campsite", back_populates="park", cascade="delete")

    @validates("entrance_fee")
    def validate_entrance_fee(self, key, fee):
        if not MIN_FEE <= fee <= MAX_FEE:
            raise ValueError("Fee must be between 13.99 and 25 inclusive")
        return fee

    def __repr__(self):
        return f"<Park ID: {self.id} Name: {self.name} >"


class Campsite(db.Model, SerializerMixin):
    __tablename__ = "campsites"

    serialize_rules = ("-park.campsites", "-created_at", "-updated_at")

    id = db.Column(db.Integer, primary_key=True)
    max_capacity = db.Column(db.Integer)
    type = db.Column(db.String)
    site_fee = db.Column(db.Float)
    has_water = db.Column(db.Boolean)
    has_bathroom = db.Column(db.Boolean)
    has_grill = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    park_id = db.Column(db.Integer, db.ForeignKey("parks.id"))

    park = db.relationship("Park", back_populates="campsites")

    @validates("max_capacity")
    def validate_max_capacity(self, key, capacity):
        if capacity > MAX_CAPACITY:
            raise ValueError("Maximum capacity is 10 people")
        return capacity

    @validates("type")
    def validate_type(self, key, type):
        if not type in SITE_TYPES:
            raise ValueError("Type must be 'tent' or 'RV'")
        return type

    def __repr__(self):
        return f"<Campsite Id: {self.id} Park: {self.park.name} Max Capacity: {self.max_capacity} >"
