import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from keys import SECRET_KEY

# app config and api setup
app = Flask(__name__)
@app.route("/api", methods=["GET"])
def get_api_status():
    return "Api v1"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", 'sqlite:///data.db')
app.secret_key = os.environ.get("SECRET_KEY", SECRET_KEY)
api = Api(app)

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
