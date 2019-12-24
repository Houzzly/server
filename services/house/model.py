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

    # finds matching user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    def __init__(self, name, bedrooms, bathrooms, close_to_river, distance_from_town, area_demographic, user_id):
        self.name = name
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.close_to_river = close_to_river
        self.distance_from_town = distance_from_town
        self.area_demographic = area_demographic
        self.user_id = user_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "rooms_coefficient": self.rooms_coefficient,
            "close_to_river": self.close_to_river,
            "close_to_river_coefficient": self.close_to_river_coefficient,
            "distance_from_town": self.distance_from_town,
            "distance_from_town_coefficient": self.distance_from_town_coefficient,
            "area_demographic": self.area_demographic,
            "area_demographic_coefficient": self.area_demographic_coefficient,
            "user_id": self.user_id
        }

    @classmethod
    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
