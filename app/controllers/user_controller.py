from flask_restful import Resource, marshal_with, Api, marshal
from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
from app.models.pagination_model import PaginationReq, PaginationAllApproval
from app.services.user_service import UserService
from flask import Blueprint, request
from app.models.users.users_req_model import UserSchema, ResendLoginSchema, ResetPasswordSchema, DataPribadiSchema, \
    DataKontakSchema, FCMToken
from app.models.users.users_res_model import users_pagination_fields, posibe_user_pic, user_field, data_pribadi_fields, \
    data_kontak_fields, data_karyawan_fields, users_cuti_kuota_pagination_fields, user_by_pic_field, \
    all_approval_fields, simple_user_field
from marshmallow import ValidationError
from app.utils.app_constans import AppConstants

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')
user_api = Api(user_bp)


class UserListController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
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
            return marshal(response, users_pagination_fields), 200
        except ValidationError as e:
            return {"message": e.messages}, 400
        except Exception as e:
            return {"message": "Internal server error"}, 500

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
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

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
    def get(self, id):

        users = UserService.get_user_by_id(id)
        if not users:
            return {"message": "User not found"}, 404
        return marshal(users, user_field), 200


    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
    def put(self, id):
        data = request.get_json()

        schema = UserSchema()

        validated = schema.load(data)

        response = UserService.update_user(id, validated)

        return response, 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
    def delete(self, id):
        response = UserService.non_active_user(id)
        return response, 200


class UserUtilController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
    def get(self):
        nip = UserService.get_latest_nip()

        return {"nip": nip}, 200


class UserGetPIC(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
    def get(self, id):
        print("Get Posible PIC From jabatan id: " + id)
        response = UserService.get_posible_pic(id)
        return marshal(response, posibe_user_pic), 200


class ResendLoginData(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
    def post(self):
        data = request.get_json()

        schema = ResendLoginSchema()

        validated = schema.load(data)

        response = UserService.resend_login_data(validated['user_id'])

        return response, 200

class ResetPasswordController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        username = get_jwt_identity()
        json_data = request.get_json()

        schema = ResetPasswordSchema()

        validated = schema.load(json_data)

        response = UserService.change_password(username, validated)

        return response, 200

class EditDataPribadiUserController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def put(self):
        username = get_jwt_identity()
        json_data = request.get_json()

        schema = DataPribadiSchema()

        validated = schema.load(json_data)

        response = UserService.edit_data_pribadi(username, validated)

        return response, 200

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        username = get_jwt_identity()

        response = UserService.get_data_pribadi(username)

        return marshal(response, data_pribadi_fields), 200

class EditDataKontakUserController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def put(self):
        username = get_jwt_identity()
        json_data = request.get_json()

        schema = DataKontakSchema()

        validated = schema.load(json_data)

        response = UserService.edit_data_kontak(username, validated)

        return response, 200

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        username = get_jwt_identity()

        response = UserService.get_data_kontak(username)

        return marshal(response, data_kontak_fields), 200

class DataKaryawanUserController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        username = get_jwt_identity()

        response = UserService.get_data_karyawan(username)

        return marshal(response, data_karyawan_fields), 200

class CreateUserAdmin(Resource):
    def post(self):
        UserService.create_user_admin()

        return None, 201

class UserListKuotaCutiController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_usr")
    def get(self):
        queryparams = request.args
        schema = PaginationReq()

        validated = schema.load(queryparams)

        print(f"Fetching all user page={validated['page']}, per_page={validated['size']}")

        data = UserService.get_users_pagination_kuota_cuti(validated['page'], validated['size'], validated['search'])

        response = {
            "pages": data.pages,
            "total": data.total,
            "items": data.items
        }
        return marshal(response, users_cuti_kuota_pagination_fields), 200

class GetUserByPic(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        username = get_jwt_identity()

        result = UserService.get_users_by_pic_id(username)

        response = {
            'items': result
        }

        return marshal(response, user_by_pic_field), 200

class UpdateFCMTokenController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        username = get_jwt_identity()
        json_data = request.get_json()

        schema = FCMToken()

        validated = schema.load(json_data)

        response = UserService.update_fcm_token_user(username, validated)

        return response, 200

class AllApprovalByApprovalUserController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        username = get_jwt_identity()
        params = request.args

        schema = PaginationAllApproval()

        validated = schema.load(params)

        response = UserService.get_waiting_by_approvals_user(username, validated)

        return marshal(response, all_approval_fields), 200

class FindUserController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        params = request.args

        response = UserService.find_user_by_username_or_name(params.get('search'))

        return marshal(response, simple_user_field), 200


user_api.add_resource(UserListController, '')
user_api.add_resource(UserController, '/<string:id>')
user_api.add_resource(UserGetPIC, '/posible-pic/<string:id>')
user_api.add_resource(UserUtilController, '/latest-nip')
user_api.add_resource(ResendLoginData, '/resend-login-data')
user_api.add_resource(ResetPasswordController, '/change-password')
user_api.add_resource(EditDataPribadiUserController, '/data-pribadi')
user_api.add_resource(EditDataKontakUserController, '/data-kontak')
user_api.add_resource(DataKaryawanUserController, '/data-karyawan')
# user_api.add_resource(CreateUserAdmin, '/init-user')
user_api.add_resource(UserListKuotaCutiController, '/kuota-cuti')
user_api.add_resource(GetUserByPic, '/users-by-pic')
user_api.add_resource(UpdateFCMTokenController, '/update-fcm-token')
user_api.add_resource(AllApprovalByApprovalUserController, '/all-approval-by-approval-user')
user_api.add_resource(FindUserController, '/find-user')