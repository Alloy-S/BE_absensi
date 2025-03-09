from flask_restful import Resource, reqparse, fields, marshal_with, abort
from services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users_model import user_fields, user_args

class UserListController(Resource):
     # method_decorators = [jwt_required()]
     
    @marshal_with(user_fields)
    def get(self):
        users = UserService.get_all_users()
        print(users)
        return users if users else {"message": "User not found"}, 200
    
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        new_user = UserService.create_user(args["name"], args["email"])
        return new_user, 201

class UserController(Resource):
    # method_decorators = [jwt_required()]
    
    
    @marshal_with(user_fields)
    def get(self, id):
        user = UserService.get_user_by_id(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    def put(self, id):
        args = user_args.parse_args()
        updated_user = UserService.update_user(id, args["name"], args["username"])
        if not updated_user:
            abort(404, message="User not found")
        return updated_user

    def delete(self, id):
        success = UserService.delete_user(id)
        if not success:
            abort(404, message="User not found")
        return {'message': 'User deleted successfully'}, 200

