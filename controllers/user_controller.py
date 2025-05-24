from flask_restful import Resource, marshal_with, Api
from services.user_service import UserService
from flask import Blueprint, request
from models.users.users_req_model import UserSchema
from models.users.users_res_model import user_fields
from marshmallow import ValidationError

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')
user_api = Api(user_bp)

class UserListController(Resource):
     # method_decorators = [jwt_required()]
     
    # @marshal_with(user_fields)
    def get(self):
        users = UserService.get_all_users()
        print(users)
        return users if users else {"message": "User not found"}, 200


    

    def post(self):

        data = request.get_json()

        schema = UserSchema()
        try:
            validated = schema.load(data)
            print(validated)

            result = UserService.create_user(fullname=validated['fullname'], data_pribadi=validated['data_pribadi'], data_kontak=validated['data_kontak'], data_karyawan=validated['data_karyawan'])


        except ValidationError as e:
            return {"message": e.messages}, 400
        except Exception as e:
            return {"message": "Terjadi Kesalahan pada Server"}, 500
        # new_user = UserService.create_user(args["name"], args["username"], args["phone"])
        return None, 201

# class UserController(Resource):
#     # method_decorators = [jwt_required()]
#
#     @marshal_with(user_fields)
#     def get(self, id):
#         users = UserService.get_user_by_id(id)
#         if not users:
#             abort(404, message="User not found")
#         return users
#
#     @marshal_with(user_fields)
#     def put(self, id):
#         args = user_args.parse_args()
#         updated_user = UserService.update_user(id, args["name"], args["username"])
#         if not updated_user:
#             abort(404, message="User not found")
#         return updated_user
#
#     @staticmethod
#     def delete(self, id):
#         success = UserService.delete_user(id)
#         if not success:
#             abort(404, message="User not found")
#         return {'message': 'User deleted successfully'}, 200

class UserUtilController(Resource):

    def get(self):
        nip = UserService.get_latest_nip()
        
        return {"nip": nip}, 200

user_api.add_resource(UserListController, '')
# user_api.add_resource(UserController, '/<string:id>')
user_api.add_resource(UserUtilController, '/latest-nip')