import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta
from flask_cors import CORS

from db import db
from keys import SECRET_KEY

from services.user.resource import UserRegister, User
from services.user.helpers import authenticate, identity
from services.house.resource import House

# app config and api setup
app = Flask(__name__)
CORS(app)
@app.route("/api", methods=["GET"])
def get_api_status():
    return "Api v1"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", 'sqlite:///data.db')
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", SECRET_KEY)
app.config["JWT_AUTH_URL_RULE"] = "/api/login"
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=604800)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

jwt = JWT(app, authenticate, identity)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        "access_token": access_token.decode('utf-8'),
        "user_id": identity.id,
        "first_name": identity.first_name,
        "last_name": identity.last_name
    })


api.add_resource(UserRegister, '/api/register')
api.add_resource(User, '/api/user/<string:id>')
api.add_resource(House, "/api/house/<string:id>")

if __name__ == "__main__":
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    app.run(port=5000, debug=True)
