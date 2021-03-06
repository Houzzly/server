import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from services.user.model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("firstName", type=str, required=True,
                        help="First name is required")
    parser.add_argument("lastName", type=str, required=True,
                        help="Last name is required")
    parser.add_argument("email", type=str, required=True,
                        help="Email is required")
    parser.add_argument("password", type=str, required=True,
                        help="Password is required")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_email(data["email"]):
            return {"message": "User with email of {} already exists".format(data['email'])}

        user = UserModel(data["firstName"], data['lastName'],
                         data['email'], data['password'])

        user.save_to_db()

        return {"message": "User created successfully"}, 201


class User(Resource):

    @jwt_required()
    def get(self, id):
        user = UserModel.find_by_id(id)

        if not user:
            return {"message": "User not found"}, 404

        return user.json()
