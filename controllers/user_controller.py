from flask_restful import Resource, reqparse, fields, marshal_with, abort
from services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

class Users(Resource):
    @marshal_with(user_fields)
    @jwt_required
    def get(self):
        return UserService.get_all_users()

    @marshal_with(user_fields)
    @jwt_required
    def post(self):
        args = user_args.parse_args()
        new_user = UserService.create_user(args["name"], args["email"])
        return new_user, 201

class User(Resource):
    @marshal_with(user_fields)
    @jwt_required
    def get(self, id):
        user = UserService.get_user_by_id(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    @jwt_required
    def patch(self, id):
        args = user_args.parse_args()
        updated_user = UserService.update_user(id, args["name"], args["email"])
        if not updated_user:
            abort(404, message="User not found")
        return updated_user

    @jwt_required
    def delete(self, id):
        success = UserService.delete_user(id)
        if not success:
            abort(404, message="User not found")
        return {'message': 'User deleted successfully'}, 200
