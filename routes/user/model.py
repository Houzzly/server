import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @classmethod
    def find_by_email(self, email):
        return self.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(self, _id):
        return self.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
