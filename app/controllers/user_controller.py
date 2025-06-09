from flask_restful import Resource, marshal_with, Api, marshal

from app.models.pagination_model import PaginationReq
from app.services.user_service import UserService
from flask import Blueprint, request
from app.models.users.users_req_model import UserSchema, ResendLoginSchema
from app.models.users.users_res_model import users_pagination_fields, posibe_user_pic, user_field
from marshmallow import ValidationError

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')
user_api = Api(user_bp)


class UserListController(Resource):

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

        validated = schema.load(data)
        print(validated)

        response = UserService.create_user(fullname=validated['fullname'], data_pribadi=validated['data_pribadi'],
                                         data_kontak=validated['data_kontak'],
                                         data_karyawan=validated['data_karyawan'])

        return response, 201



class UserController(Resource):

    def get(self, id):
        try:
            users = UserService.get_user_by_id(id)
            if not users:
                return {"message": "User not found"}, 404
            return marshal(users, user_field), 200
        except Exception as e:
            print("error")
            print(e)
            return {"message": "Internal server error"}, 500

    def put(self, id):
        data = request.get_json()

        schema = UserSchema()

        validated = schema.load(data)

        response = UserService.update_user(id, validated)

        return response, 200

    def delete(self, id):
        response = UserService.non_active_user(id)
        return response, 200


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

class ResendLoginData(Resource):
    def post(self):
        data = request.get_json()

        schema = ResendLoginSchema()

        validated = schema.load(data)

        response = UserService.resend_login_data(validated['user_id'])

        return response, 200


user_api.add_resource(UserListController, '')
user_api.add_resource(UserController, '/<string:id>')
user_api.add_resource(UserGetPIC, '/posible-pic/<string:id>')
user_api.add_resource(UserUtilController, '/latest-nip')
user_api.add_resource(ResendLoginData, '/resend-login-data')
