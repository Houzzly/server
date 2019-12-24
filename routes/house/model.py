from db import db


class HouseModel(db.Model):
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(510), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    rooms_coefficient = db.Column(db.Float(precision=2))
    close_to_river = db.Column(db.Boolean, nullable=False)
    close_to_river_coefficient = db.Column(db.Float(precision=2))
    distance_from_town = db.Column(db.String(510), nullable=False)
    distance_from_town_coefficient = db.Column(db.Float(precision=2))
    area_demographic = db.Column(db.String(510), nullable=False)
    area_demographic_coefficient = db.Column(db.Float(precision=2))
