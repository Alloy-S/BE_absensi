from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.models.auth.login_req import LoginReq
from app.models.auth.login_res import login_res

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')
auth_api = Api(auth_bp)


class LoginController(Resource):

    def post(self):
        schema = LoginReq()
        req = schema.load(request.get_json())
        response = AuthService.authenticate_user(req['username'], req['password'])

        return marshal(response, login_res), 200

       
auth_api.add_resource(LoginController, '/login')
