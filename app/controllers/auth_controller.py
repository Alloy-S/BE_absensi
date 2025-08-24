from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.models.auth.login_req import LoginReq
from app.models.auth.login_res import login_res
from app.filter.jwt_filter import role_required
from app.utils.app_constans import AppConstants
from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')
auth_api = Api(auth_bp)


class LoginController(Resource):

    def post(self):
        schema = LoginReq()
        req = schema.load(request.get_json())
        response = AuthService.login_user(req)

        return marshal(response, login_res), 200

class LogoutController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        username = get_jwt_identity()
        response = AuthService.logout_user(username)

        return response , 200

       
auth_api.add_resource(LoginController, '/login')
auth_api.add_resource(LogoutController, '/logout')
