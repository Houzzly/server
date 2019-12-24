from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from services.house.model import HouseModel


class House(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True,
                        help="First name is required")
    parser.add_argument("bedrooms", type=int, required=True,
                        help="Bedrooms is required")
    parser.add_argument("bathrooms", type=int, required=True,
                        help="Bathooms is required")
    parser.add_argument("closeToRiver", type=bool, required=True,
                        help="Close to river is required")
    parser.add_argument("distanceFromTown", type=str, required=True,
                        help="Distance from town is required")
    parser.add_argument("areaDemographic", type=str, required=True,
                        help="Area demographic is required")

    @jwt_required()
    def post(self):
        data = House.parser.parse_args()
        house = HouseModel(data["name"], data["bedrooms"],
                           data['bathrooms']. data["closeToRiver"],
                           data["distanceFromTown"], data['areaDemographic'])

        house.save_to_db()
        return house.json(), 201
