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
    parser.add_argument("distanceFromTown", type=str, required=True, choices=["close", "moderate", 'far'],
                        help="Distance from town is required")
    parser.add_argument("areaDemographic", type=str, required=True, choices=["poor", "moderate", 'rich'],
                        help="Area demographic is required")
    parser.add_argument("userId", type=int, required=True,
                        help="userId is required")

    @jwt_required()
    def post(self, id):
        data = House.parser.parse_args()
        house = HouseModel(data['name'], data["bedrooms"],
                           data['bathrooms'], data["closeToRiver"],
                           data["distanceFromTown"], data['areaDemographic'], data['userId'])

        house.save_to_db()
        return house.json(), 201

    def get(self, id):
        house = HouseModel.find_by_id(id)

        if not house:
            return {"message": "House not found"}, 404

        return house.json()

    def delete(self, id):
        house = HouseModel.find_by_id(id)

        if house:
            house.delete_from_db()

        return {"message": "House deleted"}

    def put(self, id):
        data = House.parser.parse_args()
        house = HouseModel.find_by_id(id)

        if house:
            house.name = data['name']
            house.bedrooms = data['bedrooms']
            house.bathrooms = data['bathrooms']
            house.close_to_river = data['closeToRiver']
            house.distance_from_town = data['distanceFromTown']
            house.area_demographic = data['areaDemographic']
        else:
            house = HouseModel(data['name'], data["bedrooms"],
                               data['bathrooms'], data["closeToRiver"],
                               data["distanceFromTown"], data['areaDemographic'], data['userId'])

        house.save_to_db()
        return house.json()
