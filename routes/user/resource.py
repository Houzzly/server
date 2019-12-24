import sqlite3
from flask_restful import Resource, reqparse
from user.model import UserModel


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
