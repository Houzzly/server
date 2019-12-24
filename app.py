import os

from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
