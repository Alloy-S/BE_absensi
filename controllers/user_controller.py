from flask_restful import Resource, marshal_with, Api

from models.pagination_model import PaginationReq
from services.user_service import UserService
from flask import Blueprint, request, jsonify
from models.users.users_req_model import UserSchema
from models.users.users_res_model import users_pagination_fields, posibe_user_pic
from marshmallow import ValidationError

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')
user_api = Api(user_bp)

class UserListController(Resource):
     # method_decorators = [jwt_required()]
     
    @marshal_with(users_pagination_fields)
    def get(self):
        try:
            queryparams = request.args
            schema = PaginationReq()

            validated = schema.load(queryparams)

            print(f"Fetching all user page={validated['page']}, per_page={validated['size']}")

            data = UserService.get_users_pagination(validated['page'], validated['size'], validated['search'])

            response = {
                "pages": data.pages,
                "total": data.total,
                "items": data.items
            }
            return response, 200
        except ValidationError as e:
            return {"message": e.messages}, 400
        except Exception as e:
            return {"message": "Internal server error"}, 500



    

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
            print(e)
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

class UserGetPIC(Resource):
    @marshal_with(posibe_user_pic)
    def get(self, id):
        try:
            print("Get Posible PIC From jabatan id: " + id)
            result = UserService.get_posible_pic(id)
            return result, 200
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error"}, 500

user_api.add_resource(UserListController, '')
# user_api.add_resource(UserController, '/<string:id>')
user_api.add_resource(UserGetPIC, '/posible-pic/<string:id>')
user_api.add_resource(UserUtilController, '/latest-nip')